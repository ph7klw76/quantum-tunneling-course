# Assess understanding, not just completion

Five separate outcomes are graded below. Use new explanations and notebook work, not copied quiz feedback. Suggested sequence: pretest before the lesson; posttest after independent lab work; delayed assessment after 14 days without rewatching first; transfer problem last. Collect confidence (0–100%) with each conceptual answer and compare calibration later. The tasks are educational instruments, not psychometrically validated tests.

## Pretest (15 minutes; retain the original answers)

1. **Concept:** An electron with E below a finite barrier is sometimes detected beyond it. Explain what a wavefunction predicts and whether its curve is the electron's path. State your confidence.
2. **Mathematics:** Write the stationary 1D Schrödinger equation. Identify units of E, V, x and kappa. Which quantities match at a finite constant-mass interface, and why?
3. **Computation:** Describe an independent check for code that returns T. Is setting R=1−T a sufficient conservation test? Explain.
4. **Evidence:** A device passes a small current through a nominal insulator. Give two possible mechanisms and one discriminating measurement.
5. **Judgment:** A fit returns one barrier height. Name two assumptions or uncertainties that limit interpreting it as a material property.

## Posttest (30 minutes plus notebook submission)

1. **Concept:** At the default parameters, T=0.142362. Predict the expected transmitted count and standard deviation for 10,000 independent electrons. Explain what happens to total energy. Distinguish density, amplitude and current.
2. **Mathematics:** Starting from the exponential and plane-wave solutions, write all four interface equations. Show why T=|t|² only for the identical-lead case; give the velocity-ratio correction when the leads differ. Calculate kappa in nm⁻¹ and T at a=0.90 nm with a dimensional check.
3. **Computation:** Submit the completed lab with changed parameters, your repaired unit-error model, exact/ODE comparison, tolerance study, a boundary residual and a current-conservation check. Explain the purpose of each check and one numerical limitation.
4. **Evidence:** An STM contrast feature changes with bias while geometric conditions are controlled. Explain why contrast cannot be interpreted as topography alone. Design a further observation and predict what two candidate explanations would imply.
5. **Judgment:** Current is exponential in nominal thickness but the morphology changes with thickness. Evaluate the causal claim “this proves direct tunneling.” Discuss confounding, uncertainty and a result that would reduce your confidence.

## Delayed retention assessment (14 days; 20 minutes)

1. Sketch and label a stationary scattering state at a finite barrier from memory. Explain why its density is constant in time but the real part need not be.
2. Derive the dimensions and energy dependence of kappa. Explain when an exponential approximation is justified and when you would use the exact result.
3. Recreate a minimal calculation of T in a blank notebook. Include an independently evaluated R or numerical comparison; then explain one test failure you intentionally induce and fix.
4. Propose a temperature/thickness/bias study and name one confound in each sweep.
5. Revisit your pretest confidence. Identify an assumption you now check and a remaining question. Record learning changes separately from scoring.

## Unfamiliar transfer problem

An organic/oxide interface has an estimated carrier effective mass 0.20 m_e, nominal thickness 0.8±0.1 nm, and a triangular barrier under bias. Two transport models fit its room-temperature current equally well: elastic tunneling and activated trap transport with unknown activation energy.

Submit: (a) the scaling of kappa with a justified constant effective mass and the interface-matching assumptions; (b) a numerical design for the triangular barrier with convergence and current checks; (c) temperature, thickness and bias measurement plans including leakage and morphology controls; (d) competing predicted trends, not merely a list of techniques; (e) uncertainty propagation or a sensitivity study for thickness and mass; and (f) an argument about parameter identifiability, additional data needed and what could falsify your preferred explanation. You may consult sources but must cite them and provide original work.

For thickness sensitivity, if the opaque-barrier approximation applies, d ln(T)/da≈−2 kappa. Explain why uncertain width can produce substantial uncertainty in inferred height. The 1D free-electron rectangular formula does not by itself solve the proposed interface.

## Separate analytic rubric (0–4 for each outcome; report all five scores)

| Outcome | 4: defensible independent work | 2: partial understanding | 0: absent or fundamentally incorrect |
| --- | --- | --- | --- |
| Concept | Distinguishes state, density, current and detection; preserves energy and avoids trajectory claims | Correct terms but confused interpretation | Classical-path or energy-loan explanation |
| Mathematics | Consistent units, boundary equations and current ratios; justified approximations | Mostly correct result with a missing assumption | Inconsistent dimensions or conditions |
| Computation | Reproducible original code, independent check, convergence and error diagnosis | Working calculation with limited checks | No executable work or unexplained copied result |
| Evidence | Compares explicit competing predictions and informative controls | Names alternatives but weak discriminating test | Treats a single current/trend as proof |
| Judgment | Quantifies sensitivity/uncertainty, discusses identifiability and revision criteria | Lists limitations without implications | Claims unique mechanism/material parameter without support |

Use 1 and 3 for intermediate performance. Suggested mastery: at least 3 in **each** outcome plus a corrected explanation of any energy-conservation or trajectory misconception. Quiz scores inform remediation but do not replace these five judgments. Use blinded marking and a second marker for research comparisons when practical; report pre/post changes, attrition and uncertainty without claiming the lesson caused improvements from an uncontrolled cohort.

## Instructor reference points (release after submission)

Default: kappa=3.622626 nm⁻¹; T=0.142361995; R=0.857638005. For N=10,000: mean≈1423.62, binomial standard deviation≈34.94. At a=0.90 nm: T≈0.00587308; ratio to default≈0.0412546. Constant mass: match psi and psi′. For distinct leads, T=(v_right/v_left)|t|² with the same incident amplitude convention; effective-mass interfaces require a suitable Hamiltonian and matching law. Thin-barrier exponential estimates are not exact. Exponential thickness trends and weak temperature dependence can support a direct-tunneling account in a controlled regime but do not uniquely establish it.
