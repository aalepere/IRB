# Credit Risk

Credit risk is the risk that a counterparty will fail to meet his payment obligation, resulting in a loss. This risk is historically considered the main risk for banks. Under BIS II a bank should asses its credit risk and retain capital for it.

# IRB - The Internal Ratings-Based Approach

## Vasicek model - http://bis2information.org/content/Vasicek_model

The formula used to determine the regulatory capital is commonly referred to as the Vasicek model. The purpose of this model is to determine the expected loss (EL) and unexpected loss (UL) for a counterparty, as explained in the previous section. The first step in this model is to determine the expected loss. This is the average credit loss. There is a 50% change of realizing this loss or less. 

The expected loss is determined using three main ingredients:
- **PD**: Probability of default, the average probability of default over a full economic cycle;
- **EAD**: Exposure at default, the amount of money owed at the moment a counterparty goes into default;
- **LGD**: Percentage of the EAD lost during a default.

The expected loss (EL) is equal to the PD times the LGD times the EAD:
EL = PD X LGD X EAD

The expected loss is half the work of the model. The EL determines (roughly) the amount of provisions which should be taken (the essence of any provision is to save money for losses you expect in the future). The second half of the work is to determine the Unexpected Loss (UL). The UL is the additional loss in atypical circumstances, for which tier capital should be retained. The Vasicek model estimates the UL by determining the PD in a downturn situation. The model assumes that the EAD and LGD are not affected by dire circumstances. Both parameters are considered constant for a company. The model calculates the loss during a downturn situation (for instance an exceptionally bad economy) by multiplying the downturn PD times the LGD times the EAD. The UL is calculated by subtracting the expected loss from the loss during a downturn situation. 

In formula’s this equates to:
UL = (PDdownturn X LGD X EAD) – (PD X LGD X EAD)

which is equal to:
UL = (PDdownturn – PD) X LGD X EAD

The PD in a downturn situation is determined using the average (through the cycle) PD. At this point Vasicek uses two different models. 

### Merton Model
First it uses the Merton model. This model states that a counterparty defaults because it cannot meet its obligations at a fixed assessment horizon, because the value of its assets is lower than its due amount. Basically it states that the value of assets serve to pay off debt. The value of a company’s assets vary through time. If the asset value drops below the total debt, the company is considered in default. This logic allows credit risk to be modelled as a distribution of asset values with a certain cut-off point (called a default threshold), beyond which the company is in default. The area under the normal distribution of the asset value below the debt level of a company therefore represents the PD.

The logic used by Merton can also be reversed. In Vasicek a PD (for instance calculated with a scorecard) is given as input. 
Instead of taking the default threshold (debt value) and inferring the PD as Merton does, Vasicek takes the PD and infers the default threshold. Vasicek does this using a standard normal distribution. This is a distribution with an average of zero and a standard deviation of one. This way the model measures how many standard deviations the current asset value is higher than the current debt level. In other words it measures the distance to default. The graph below shows that a PD of 6.68% means that the company is currently 1.5 standard deviations of its asset value away from default. By using the standard normal distribution the actual asset value, standard deviation and debt level becomes irrelevant. It is only necessary to know a PD and the distance to default can be determined.


### Gordy Model
Now that the PD has been transformed to a distance to default the second step of the model comes into play. In this step Vasicek uses the Gordy model. 
The distance to default is a through the cycle distance, because the PD used is through the cycle. In other words it is an average distance to default in an average situation. This distance to default will have to be transformed into a distance to default during an economic downturn. To do this a single factor model is used. It is assumed that the asset value of a company is correlated to a single factor. In other words, if the factor goes up the asset value goes up, if the factor goes down the asset value goes down. This factor is often referred to as the economy. This is done because it is intuitively logical that the asset value of a company is correlated to the economy. We will follow this tradition; however the factor is merely conceptual. It is assumed that there is a single common factor (whatever it may be) to which the asset value of all companies show some correlation. The common risk factor (the economy) is also assumed to be a standard normal distribution.

To recap we have a standard normal distribution representing the possible asset values, a default threshold inferred using the PD, a standard normal distribution representing the economy to which the asset value is correlated and a correlation between the economy and the asset value. Using the correlation it is possible to determine the asset value distribution given a certain level of the economy. If the economy degrades the expected asset value will also decrease shifting the asset value distribution to the left. Furthermore the standard deviation will also decrease. In other words an asset value distribution given a certain level of the economy can be calculated using the correlation between the asset value and the economy.


The degree in which the asset value distribution is deformed depends on the level of the economy which is assumed. The level of the economy is measured as the number of standard deviations the economy is from the average economy. For instance the economic level with a probability of 99.9% of occurring or better has a distance of 3.09 standard deviations from the average economy.

The new distance to default can be calculated by taking the average of the distance of the level of the economy (used to determine the downturn PD) and the distance to default, weighted by the correlation (r). 

In formula’s this equates to:
DistanceToDefaultDownturn = (1-r)^-0.5 X DistanceToDefault + (r/(1-r))^0.5 X DistanceFromEconomy.

For example the PD was 6.68% and the distance to default was -1.5. 
Now assume a counterparty has a 9% correlation to the economy. 
Secondly determine that the economic downturn level is the 99.9% worst possible economic level (used in BIS II). 
At this level the distance between the downturn level and the average economy is 3.09. 

In our equation the new distance to default (given the 99.9% worst economy) is:
-0.6 = (1-9%)^-0.5 X -1.5 + (9%/(1-9%))^0.5 X 3.09

In other words the -1.5 distance to default decreases to a distance to default of -0.6. The new PD associated with a distance to default of -0.6 is 27.4%.

Now the Vasicek model has finished its job. In short it has accomplished the following tasks:

- It has determined the loss during normal circumstances (Expected Loss) using EL = PD X LGD X EAD. Where the PD is an average PD.
- It has determined the downturn PD using DistanceToDefaultDownturn = (1-r)^-0.5 X DistanceToDefault+ (r/(1-r))^0.5 X DistanceFromEconomy.
- It has determined the Unexpected Loss using UL = (PDdownturn – PD) X LGD X EAD

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
