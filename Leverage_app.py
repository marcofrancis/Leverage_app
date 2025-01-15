import streamlit as st
from Leverage import plot_restaking_portfolios

# Set page config
st.set_page_config(
    page_title="Restaking Portfolio Analysis",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("Restaking and Leverage")
st.write("We want to investigate the relationship between restaking and leverage. In particular we want to see if we can replicate the exposure of a restaking strategy with the use of a leveraged portfolio.")

st.subheader("Restaking")
st.write("Let's suppose that we have a wealth $w$ in ETH to restake in two AVS. In this setting let's indicate with $\phi_1$ and $\phi_2$ the amount of ETH we invest in the first and second AVS.")

st.write("Each AVS will promise a certain reward, and we will face a certain risk and cost when we restake our ETH with them. To model this we will simply assume that the payoff from restaking the amount $w\phi_1$ in the first AVS is given by $w\phi_1(1+r_1)$ and similarly for the second AVS we have a payoff of $w\phi_2(1+r_2)$.")

st.write("The interesting bit about restaking is that we can increase our capital efficiency and get rewards from multiple sources for the same amount of capital invested. More precisely we can model the total reward from restaking as:")

st.latex(r"w\left[\phi_{1}\left(1+r_{1}\right)+\phi_{2}\left(1+r_{2}\right)+(1-\phi_{1}-\phi_{2})(1+r_{1}+r_{2})\right]=w\left[1+r_{1}\left(1-\phi_{2}\right)+r_{2}(1-\phi_{1})\right]")

st.write("where $0\leq \phi_1 + \phi_2 \leq 1$.")

st.subheader("Leveraged Portfolios")
st.write("Another, more classical, way to invest our capital, could be to construct a leveraged position in the two AVSs. In this case we will borrow at the risk-free rate $r_f$ and invest in the two AVSs. The payoff from this strategy will be given by:")

st.latex(r"w\left[\varphi_{1}\left(1+r_{1}\right)+\varphi_{2}\left(1+r_{2}\right)+(1-\varphi_{1}-\varphi_{2})(1+r_{f})\right]=w\left[1+\varphi_{1}r_{1}+\varphi_{2}r_{2}+\left(1-\varphi_{1}-\varphi_{2}\right)r_{f}\right]")

st.latex(r"\text{where } 0 \leq \varphi_1,\varphi_2 \leq 1")

st.header("Interactive Analysis")
st.write("Adjust the parameters using the sliders to explore different scenarios.")

# Create two columns: one for sliders and one for the plot
slider_col, plot_col = st.columns([1, 2])

# Put all sliders in the left column
with slider_col:
    mu1 = st.slider("Expected Return AVS1 (μ₁)", min_value=0.0, max_value=0.20, value=0.05, step=0.01)
    mu2 = st.slider("Expected Return AVS2 (μ₂)", min_value=0.0, max_value=0.20, value=0.07, step=0.01)
    sigma1 = st.slider("Volatility AVS1 (σ₁)", min_value=0.01, max_value=0.50, value=0.10, step=0.01)
    sigma2 = st.slider("Volatility AVS2 (σ₂)", min_value=0.01, max_value=0.50, value=0.15, step=0.01)
    rf = st.slider("Risk-Free Rate", min_value=0.0, max_value=0.10, value=0.02, step=0.01)
    rho = st.slider("Correlation (ρ)", min_value=-1.0, max_value=1.0, value=0.3, step=0.1)

# Put the plot in the right column
with plot_col:
    fig = plot_restaking_portfolios(
        mu1=mu1, mu2=mu2, sigma1=sigma1,
        sigma2=sigma2, rho=rho, rf=rf,
        n_points=105
    )
    st.pyplot(fig)

st.subheader("Notes:")
st.write("""
- **Non-Leveraged Portfolios** (circles): Traditional portfolios where total allocation ≤ 100%
- **Leveraged Portfolios** (triangles): Portfolios that allow borrowing at the risk-free rate
- Color intensity indicates allocation levels for both portfolio types
""") 