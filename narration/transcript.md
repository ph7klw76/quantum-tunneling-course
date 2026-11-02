# Can an Electron Pass Through a Wall?

## 00:00 — Can an electron pass through a wall?

Can an electron pass through a wall? For a carefully defined potential barrier, yes. Today we will calculate the probability, test our calculation, and ask what evidence could actually support that conclusion. Imagine a finite potential barrier: a wall in an energy diagram, rather than an everyday brick wall.

## 00:19 — Start with a classical prediction

Our electron has half an electron volt of energy. The barrier is one electron volt high and zero point four five nanometers wide. Classically, the electron cannot reach the top, so it returns. We use zero potential outside, so the total energy there is kinetic energy.

## 00:37 — Pause and predict

Pause and predict. In quantum mechanics, must the transmission probability also be exactly zero? Choose your answer before continuing. Explain which assumption of the classical picture you are using.

## 00:56 — A wave prediction

Quantum mechanics describes a state using a wavefunction. A finite barrier can support a nonzero transmitted probability current. This does not mean the electron secretly climbs over the barrier, or follows the curve drawn here. Detection beyond the barrier is an outcome; transmission predicts how often we expect it.

## 01:16 — What the curves mean

The cyan curve is the real part of a stationary scattering wavefunction, multiplied by its time dependent phase. Gold shows its probability density. The density is time independent here. A single detection is localized, while these curves describe the statistics of many identically prepared measurements. Changing the phase changes the real part, while a stationary probability density stays fixed.

## 01:41 — Incident plus reflected

On the left, an incoming wave and a reflected wave overlap. Their interference makes the density ripple. On the right, only an outgoing wave is present. Our incident amplitude is one, so these scattering states are not normalized to one over all space. Transmission is a ratio of probability currents. Interference changes the density on the left, while the net probability current remains constant.

## 02:06 — Pause: what must match?

Pause and predict. At each edge of this finite barrier, which quantities must be continuous? The wavefunction alone? The wavefunction and its spatial derivative? Or the potential itself? Our model has a constant electron mass and no delta function potential. Keep those assumptions in your reasoning.

## 02:31 — Four boundary conditions

Both the wavefunction and its first spatial derivative are continuous at each edge. There are four matching equations for four unknown amplitudes. The potential may jump. For interfaces described by different effective masses, the matching law needs a suitable effective mass model; do not copy these conditions without checking its assumptions. Integrating the equation across a shrinking interval gives the derivative condition for a finite step.

## 02:57 — The stationary Schrödinger equation

The time independent Schrödinger equation relates the curvature of the wavefunction to the difference between potential and total energy. Here, h-bar is Planck's constant divided by two pi. Outside the barrier the solutions oscillate. Inside, where the energy is lower than the potential, the solutions are exponentials. The decay constant kappa has units of inverse length. Notice how the sign of the curvature distinguishes the oscillatory and exponential regions.

## 03:27 — Evanescent does not mean absent

A finite barrier requires a combination of two exponential solutions, not just one decaying exponential. Matching the two interfaces produces the transmitted wave. In this stationary model total energy is conserved. The electron does not borrow energy, and the uncertainty principle is not a license to violate energy conservation. The complex coefficients of those exponentials together allow a conserved current inside the barrier.

## 03:55 — Pause: read a probability

Suppose the calculated transmission coefficient is about zero point one four. Does that mean every electron loses fourteen percent of its energy? Or that around fourteen percent of a large incident ensemble is transmitted? Predict an outcome for ten thousand independent electrons. Include the fact that a finite count will fluctuate.

## 04:22 — The exact rectangular-barrier result

The exact expression on screen gives about zero point one four for our default parameters. Roughly fourteen hundred of ten thousand incident electrons are expected to transmit, with statistical fluctuations. Equal potentials and equal masses on both sides mean the transmitted amplitude squared equals transmission. Reflected and transmitted currents add to the incident current. An individual trial gives one detection outcome. Repeating the preparation makes the probability prediction testable.

## 04:51 — Thin versus thick

Now hold energy and barrier height fixed while changing width. Notice how the outgoing amplitude shrinks as the barrier thickens. The wavefunction is calculated by matching both interfaces each time. The animation changes the model between stationary solutions; it is not a simulation of a moving wall or an electron trajectory. At a quarter nanometer, transmission is about forty eight percent; at zero point six five, about three and a half percent.

## 05:18 — Why width matters so much

When kappa times width is large, transmission falls approximately exponentially with width. The prefactor still depends on energy and height. Use the exact expression when the barrier is not opaque. Taking a logarithm turns the approximate exponential trend into a line, which is useful when designing measurements. The factor of two in the exponent comes from squaring the magnitude of an amplitude.

## 05:43 — Pause: double the width

Pause and predict. At fixed energy and height, does doubling barrier width simply cut transmission in half? Or can it reduce transmission much more strongly? Write the ratio you would calculate using the exact formula. Do not assume the exponential approximation is exact for the thinner barrier.

## 06:08 — Calculate, then cross-check

For widths zero point four five and zero point nine nanometers, transmission drops from about fourteen percent to about zero point six percent. In the laboratory, compare the closed form with independent differential equation integration. Also check continuity and constant probability current. Defining reflection as one minus transmission alone would not independently test conservation. Two implementations can share the same unit error. That is why dimensions and limiting cases also matter.

## 06:40 — Raise the electron energy

Raising energy toward the barrier height increases transmission in this below barrier model. But do not extrapolate this equation past its stated domain. At or above the barrier, use the correct limiting expression or the oscillatory solution. As the energy gap shrinks, the decay length grows, allowing more amplitude to reach the exit.

## 07:00 — Raise the barrier height

A higher barrier increases the decay constant and reduces transmission for these fixed parameters. Width, height, and effective mass all matter. In an actual device, voltage can change the barrier shape as well as the occupied electron energies. Always convert the energy and length units consistently before evaluating an exponential.

## 07:22 — Pause: an energy loan?

Pause and predict. Does tunneling require the electron to borrow extra energy? Check your answer against our time independent equation, which has one fixed total energy on both sides. The wave inside the barrier does not describe a classical trajectory.

## 07:44 — Energy stays conserved

No energy loan is required. For our static, elastic, lossless barrier, transmitted and reflected electrons have the same total energy as the incident electrons. Interactions that exchange energy require a richer model. The decaying amplitude is compatible with one conserved energy throughout this elastic scattering problem.

## 08:05 — Scanning tunneling microscopy

In scanning tunneling microscopy, a conducting tip approaches a conducting sample. A small bias allows a net tunneling current across the vacuum gap. Because transmission is sensitive to separation, a feedback loop can adjust tip height to maintain a chosen current as the tip scans across the surface. The tip can carry a current without touching the sample: that is the practical opportunity.

## 08:32 — What an STM image represents

The resulting image is not simply a photograph of hard atomic surfaces. The current depends on electronic states, bias, and tip properties as well as separation. Our rectangular barrier captures a useful sensitivity, but a realistic current calculation must include occupied states, empty states, and the energy window selected by the bias. An apparent hill in a current map can therefore reflect electronic structure as well as geometry.

## 08:59 — Pause: interpret the image

Pause and predict. If the current doubles in your measurement, has the surface height necessarily doubled? Consider a different tip, a change of local electronic states, and a different bias. Which controlled comparisons would help distinguish geometry from electronic contrast? Write a prediction before you reveal the feedback.

## 09:25 — Electronic interfaces

No simple doubling rule connects current and height. Semiconductor oxides and organic electronic interfaces also have complicated transport: direct tunneling may compete with thermally activated injection, hopping, and trap assisted processes. Effective masses, nonrectangular barriers, inelastic scattering, and distributions of molecular arrangements can all matter. A fitted barrier is a model parameter, not automatically a measured material constant. In an organic layer, molecular orientation and disorder can also change the available pathways.

## 10:00 — Build an evidence argument

A small current through a nominally insulating layer is evidence of transport, but it does not identify a unique mechanism. Measure a thickness series and a temperature series. Control contact area, defects, and instrument leakage. Compare multiple plausible models and examine their residuals, rather than judging only whether one curve looks convincing. Choose measurements where the competing mechanisms make different, observable predictions.

## 10:27 — Pause: is one trend conclusive?

Pause and predict. An exponential decrease of current with thickness is observed. Does that conclusively prove direct tunneling? Consider whether defects, thickness dependent morphology, or another transport mechanism could generate a similar trend. State one additional measurement and explain what competing predictions it would test.

## 10:53 — Evidence can support without proving

The trend supports a tunneling explanation, but is not conclusive by itself. Weak temperature dependence under controlled conditions can strengthen the case for direct elastic tunneling, while thermally activated behavior motivates alternatives. No single signature is universal. Report parameter uncertainty, measurement limits, model assumptions, and what observation would make you change your explanation. Confidence grows from consistent evidence across conditions, rather than from one successful fit.

## 11:24 — Your turn: calculate and investigate

Open the companion laboratory. Predict first, change the parameters, and compare analytical and numerical results. Then design an experiment for an unfamiliar interface. Submit your own explanations, code, uncertainty analysis, and reflection. Completing a quiz is practice, not proof of understanding. The goal is to make a defensible scientific judgment and know where your model ends. Connect a physical assumption, a numerical check, and a measurement that could change your conclusion.
