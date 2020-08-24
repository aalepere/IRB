# IRB - The Internal Ratings-Based Approach

## Basel IRB

The IRB approach allows the internal specifications of key model parameters such as unconditional default probabilites, exposures at rik (EAD) and Loss Given Default (LGD).

Basel II/III recommend that financial institutions adopt the IRB approach for computation of regulatory capital.

One of the key assumption made in the IRB approach is **portfolio invariance**. The portfolio invariance principle, assumes that the risk of the overall portfolio depends only on the characteristics of all individual exposures and therefore independt from the portfolio structure.

## The basic structure

In the credit-default risk setting, it is assumed that the pricing of these instruments accounts for expected default losses. The main idea of economic capital is to create a link between theses unexpected losses and the amount of capital held by the instituion.
As described in the previous section, the assumption of portfolio invariance implies that each credit counterparty computes its own contribution to the overall risk capital.

We can denote the risk-capital contribution of the *nth* obligor as RCn(alpha) where alpha is level of confidence (for IRB 99.9%). Therefore, the total risk-capital can ne defined as:

<img src="https://render.githubusercontent.com/render/math?math=RC\alpha = \sum_{n=1}^{N} RCn(\alpha)">
where N represents the number of obligors in the portfolio.

According to the current Basel IRB guidance, the risk-capital contribution of the *nth* obligor is denoted as:

<img src="https://render.githubusercontent.com/render/math?math=RCn(\alpha) = \mu n * K\alpha(n)">
where mun detones the obligor exposure and equal to EAD * LGD.

Unexpected Loss (UL) = Worst Case Loss - Expected Loss
                     = VaR(alpha) - EL
The unexpected loss is thus essentially the worst-case loss, for a given level of confidence, less the expected default loss. 

We have defined Kalpha(n) as the *nth* risk-capital contribution. Practically, it is a function of two main arguments: the unconditional default probability, pn , and the tenor, or term to maturity, of the underlying credit obligation denoted Mn.

<img src="https://render.githubusercontent.com/render/math?math=K\alpha(Tenor, PD)=EAD*LGD*(Conditional Default Probability - Unconditional Default Probability)*MaturityAdjustement">
<img src="https://render.githubusercontent.com/render/math?math=K\alpha(Tenor, PD)=EAD*LGD*(PD(\Phi^-1(\alpha)) - PD)*Ma">
