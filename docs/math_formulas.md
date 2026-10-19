# Mathematical Formulas of Ω-RE

## Basic Definitions

### Rate of self-actualization
\[
\Omega = \frac{1}{\Phi}\frac{d\Phi}{dt}
\]

### Ω-spectrum of a theory
\[
T(\Omega) = \int S_T(\omega)\,e^{i\omega\Omega}\,d\omega
\]

### Φ-spectrum
\[
T(\Phi) = \int S_T(\varphi)\,e^{i\varphi\Phi}\,d\varphi
\]

### Relation of spectra (Fourier)
\[
S_T(\omega) = \int S_T(\varphi)\,e^{-i\varphi\omega}\,d\varphi
\]

## Resonance

### Normalized cross-correlation
\[
R_\Omega(T_1,T_2)=\frac{\bigl|\int S_{T_1}(\omega)S_{T_2}^*(\omega)\,d\omega\bigr|^2}{\bigl(\int|S_{T_1}|^2\,d\omega\bigr)\bigl(\int|S_{T_2}|^2\,d\omega\bigr)}
\]

### Resonant band
\[
B(T_1,T_2)=\{\Omega:R_\Omega(T_1,T_2)>R_{\mathrm{threshold}}\}
\]
Default \(R_{\mathrm{threshold}}=0.8\).

### Dynamic resonance
\[
\frac{dR_\Omega}{dt}=\frac{\partial R_\Omega}{\partial\Omega}\cdot\frac{d\Omega}{dt}
\]

## Emergent kernel
\[
K(T_1\to T_2,\Omega)=\frac{S_{T_2}(\omega)}{S_{T_1}(\omega)}
\]

## Substrate*
At \(\Phi=1\):
\[
R_\Omega(T_i,T_j)=1\quad\forall\,i,j
\]
