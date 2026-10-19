# Ω-RE Algorithm – 6 Steps

## 1. Spectral Decomposition
For every theory \(T\):
1. Identify fundamental frequencies (eigenvalues of the evolution operator).
2. Assign spectral weights \(|c_n|^2\).
3. Normalize \(\int|S_T|^2\,d\omega=1\).

**Output:** \(S_T(\omega)\) for each theory.

## 2. Resonance Computation
For every pair \(T_1,T_2\):
1. Compute the cross-correlation of spectra.
2. Normalize to \([0,1]\).
3. Store in the resonance matrix.

**Output:** Matrix \(R[i,j]\).

## 3. Band Identification
For every pair:
1. Find intervals of \(\Omega\) where \(R_\Omega>R_{\mathrm{threshold}}\).
2. Determine center, width and maximum of each band.

**Output:** Registry \(B(T_1,T_2)\).

## 4. Emergent Derivation
For every band:
1. Compute the kernel \(K=S_{T_2}/S_{T_1}\).
2. Apply the kernel to the equations of \(T_1\).
3. Verify consistency with \(T_2\).

**Output:** Derivation map.

## 5. Prediction Generation
For every band:
1. Compute deviations from the standard theory.
2. Determine falsification conditions.
3. Store predictions.

**Output:** Prediction registry.

## 6. Feedback
After an experiment:
- Prediction confirmed → strengthen the band, add new predictions.
- Prediction falsified → weaken the band, remove predictions.
- Undecided → keep, wait for more data.

**Output:** Updated resonance registry.
