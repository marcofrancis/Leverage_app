import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def plot_restaking_portfolios(mu1=0.05, mu2=0.07, sigma1=0.10, sigma2=0.15, rho=0.3, rf=0.02, n_points=100):
    """
    Plot attainable portfolios for restaking strategies with two AVS options and their leveraged counterparts.
    
    Parameters:
    -----------
    mu1 : float
        Expected return for AVS1 (default: 0.05)
    mu2 : float
        Expected return for AVS2 (default: 0.07)
    sigma1 : float
        Volatility for AVS1 (default: 0.10)
    sigma2 : float
        Volatility for AVS2 (default: 0.15)
    rho : float
        Correlation between AVS1 and AVS2 (default: 0.3)
    rf : float
        Risk-free rate (default: 0.02)
    n_points : int
        Number of points to generate for the grid (default: 200)
    
    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object containing two subplots
    """
    # Covariance between AVS1 and AVS2
    cov = rho * sigma1 * sigma2

    # Generate points more efficiently using vectorization
    phi1 = np.linspace(0, 1, n_points)
    phi2 = np.linspace(0, 1, n_points)
    phi1_grid, phi2_grid = np.meshgrid(phi1, phi2)

    # -------------------------------------------------------------------------
    # Non-Leveraged Portfolios - Vectorized calculations
    # -------------------------------------------------------------------------
    
    # Calculate returns and volatility for all points at once
    E_R = mu1 * (1 - phi2_grid) + mu2 * (1 - phi1_grid)
    
    Var_R = (1 - phi2_grid)**2 * sigma1**2 + \
            (1 - phi1_grid)**2 * sigma2**2 + \
            2 * (1 - phi1_grid) * (1 - phi2_grid) * cov
    sigma_R = np.sqrt(Var_R)

    # Create mask for valid portfolios
    valid_mask = (phi1_grid + phi2_grid <= 1)
    zero_alloc_mask = np.abs(1 - phi1_grid - phi2_grid) < 1e-10

    # -------------------------------------------------------------------------
    # Leveraged Portfolios - Vectorized calculations
    # -------------------------------------------------------------------------
    
    E_R_leverage = phi1_grid * mu1 + phi2_grid * mu2 + \
                   (1 - phi1_grid - phi2_grid) * rf
    
    Var_R_leverage = phi1_grid**2 * sigma1**2 + \
                     phi2_grid**2 * sigma2**2 + \
                     2 * phi1_grid * phi2_grid * cov
    sigma_R_leverage = np.sqrt(Var_R_leverage)

    # -------------------------------------------------------------------------
    # Plotting with Matplotlib
    # -------------------------------------------------------------------------
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot non-leveraged portfolios
    scatter1 = ax.scatter(
        sigma_R[valid_mask & ~zero_alloc_mask],
        E_R[valid_mask & ~zero_alloc_mask],
        c=1 - phi1_grid[valid_mask & ~zero_alloc_mask] - phi2_grid[valid_mask & ~zero_alloc_mask],
        cmap='Blues_r',
        s=10,
        alpha=0.8,
        label='Restaking'
    )
    
    # Plot fully allocated portfolios
    ax.scatter(
        sigma_R[valid_mask & zero_alloc_mask],
        E_R[valid_mask & zero_alloc_mask],
        c='blue',
        s=10,
        alpha=1,
        zorder=3,
        label='Restaking with(1 - φ1 - φ2)=0'
    )
    
    # Plot leveraged portfolios
    scatter2 = ax.scatter(
        sigma_R_leverage,
        E_R_leverage,
        c=phi1_grid + phi2_grid,
        cmap='Reds_r',
        s=10,
        alpha=0.1,
        label='Leveraged'
    )

    # Add colorbars with alpha=1
    scatter2.set_alpha(1)  # Temporarily set alpha to 1 for colorbar
    cbar2 = plt.colorbar(scatter2, ax=ax, label='Leverage (φ1 + φ2)')
    scatter2.set_alpha(0.1)  # Reset alpha for main plot
    
    scatter1.set_alpha(1)  # Temporarily set alpha to 1 for colorbar
    cbar1 = plt.colorbar(scatter1, ax=ax, label='Capital in both AVSs (1 - φ1 - φ2)')
    scatter1.set_alpha(0.8)  # Reset alpha for main plot
    
    # Set labels and title
    ax.set_xlabel('Volatility (Standard Deviation)')
    ax.set_ylabel('Expected Return')
    ax.set_title('Non-Leveraged vs Leveraged Portfolios: Expected Return vs Volatility')
    
    # Add grid and legend with solid colors
    ax.grid(True, alpha=0.3)
    restaking = mlines.Line2D([], [], color='#6caed6', marker='o', ls='', label='Restaking')
    restaking_with_zero = mlines.Line2D([], [], color='blue', marker='o', ls='', label='Restaking with (1 - φ1 - φ2)=0')
    leveraged = mlines.Line2D([], [], color='#fb6b4b', marker='o', ls='', label='Leveraged')
    plt.legend(handles=[restaking, restaking_with_zero, leveraged])

    # Adjust layout
    plt.tight_layout()
    
    return fig