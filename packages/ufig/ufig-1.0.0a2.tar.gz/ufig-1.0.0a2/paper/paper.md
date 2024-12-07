---
title: 'UFig v1.0.0: The ultra-fast image generator'
tags:
  - Python
  - astronomical images
  - cosmology
  - GalSBI
authors:
  - name: Silvan Fischbacher
    orcid: 0000-0003-3799-4451
    affiliation: 1
    equal-contrib: true
  - name: Beatrice Moser
    orcid: 0000-0001-9864-3124
    affiliation: 1
    equal-contrib: true
  - name: Tomasz Kacprzak
    orcid: 0000-0001-5570-7503
    affiliation: "1, 2"
    equal-contrib: true
  - name: Luca Tortorelli
    affiliation: "1, 3"
    equal-contrib: true
    orcid: 0000-0002-8012-7495
  - name: Joerg Herbel
    affiliation: 1
    equal-contrib: true
  - name: Joel Berge
    orcid: 0000-0002-7493-7504
    affiliation: "1, 4"
  - name: Lukas Gamper
    affiliation: 1
  - name: Claudio Bruderer
    affiliation: 1
  - name: Uwe Schmitt
    affiliation: 1
    orcid: 0000-0003-3416-9317
  - name: Adam Amara
    affiliation: "1,5"
    orcid: 0000-0003-3481-3491
  - name: Alexandre Refregier
    orcid: 0000-0003-3416-9317
    affiliation: 1

affiliations:
 - name: ETH Zurich, Institute for Particle Physics and Astrophysics, Wolfgang-Pauli-Strasse 27, 8093 Zurich, Switzerland
   index: 1
 - name: Swiss Data Science Center, Paul Scherrer Institute, Forschungsstrasse 111, 5232 Villigen, Switzerland
   index: 2
 - name: University Observatory, Faculty of Physics, Ludwig-Maximilian-Universität München, Scheinerstrasse 1, 81679 Munich, Germany
   index: 3
 - name: DPHY, ONERA, Université Paris Saclay, F-92322 Châtillon, France
   index: 4
 - name: School of Mathematics and Physics, University of Surrey, Guildford, Surrey, GU2 7XH, UK
   index: 5

date: XXXX-XX-XX
bibliography: paper.bib
---

# Summary

With the rise of simulation-based inference (SBI) methods, simulations should not only be accurate but also fast.
UFig is a Python package that accounts for this need by generating simulated astronomical images extremely fast at the order of the time required to extract the sources from this image.
To render an images, UFig requires a catalog of galaxies, and a description of the point spread function (PSF) of the image.
Further features include the possibility to add background noise, to sample and render stars using the Besancon model of the Milky Way [@besancon], to run SExtractor [@sextractor] to extract sources from the rendered image, to match the extracted sources to the input catalog using the method described in @moser, to add flags to all the sources based on the SExtractor output and passed survey masks, and to run the emulators to surpass the image simulation and extraction steps [@fischbacher].
A first version of UFig was presented in @ufig and the software was used and further developped in many projects of the GalSBI framework [@herbel;@kacprzak;@tortorelli1;@tortorelli2;@moser;@fischbacher].

# Statement of need

UFig is a crucial part of the GalSBI framework.
GalSBI is a galaxy population model that is used to generate mock galaxy catalogs for all kind of cosmological applications such as photometric redshift distribution, shear and blending calibration or to forward model selection effects.
Constraining this model is done by comparing the mock catalogs to the observed data.
To accurately compare the simulations with the data, the simulations need to be as realistic as possible.
We therefore need to include systematic and observational effects such as the PSF and the background noise of the data, as well as the survey masks.
This can be done by rendering images from the GalSBI catalogs and extracting the sources from the images with the same method as for the data.

Since the dimensionalty of the parameter space of the galaxy population model is high (around 50 parameters) and the numbers of simulations required to constrain the model is hence large, a fast image generator is crucial to make the inference feasible.
UFig's rendering implementation is based on a combination of pixel-based and photon-based rendering methods, which allows for a fast rendering of the images (see @ufig for more details).
The rendering time of UFig is at the order of the time required to extract the sources from the image, which is much faster than other image simulations while still including all the necessary effects for most cosmological applications.
This balance makes UFig unique in the field of image simulation compared to other software packages (e.g. GalSim [@galsim], ImSim [@imsim], Skymaker [@skymaker] or the GREAT challenge simulations [@great3;@great8;@great10]).
To flexibly adapt to different use cases, UFig is based on the `ivy` workflow engine and provides plugins for the different steps of the image generation process.
The full workflow can then be defined in a single configuration file, where the user can specify which plugins to use and how to configure them, e.g. by defining the PSF or background model, making the image generation process flexible and easy to use.

Compared to the first version of UFig presented in @ufig, new features and improvements have been added.
@bruderer used UFig to render DES-like images for which the PSF modeling and the background noise were adapted to the DES data.
Furthermore, to ensure a realistic distributions of the stars in the images, a plugin to sample stars from the Besancon model of the Milky Way [@besancon] was added.
@herbel constrained a galaxy population model using UFig.
This galaxy population model was then used to measure cosmic shear in @kacprzak.
This effort required major improvements in the background and PSF modelling.
The PSF modelling based on a convolutional neural network (CNN) was presented in @herbel_psf.
@tortorelli2 adapted UFig to render images for narrow-band filters in the context of the PAU survey.
@moser used UFig to simulate deep fields of the Hyper Suprime-Cam (HSC) which required further adaptions for the PSF modelling and the matching of the extracted sources to the input catalog.
Finally, @fischbacher introduced emulators to surpass the image simulation and extraction steps.

# Features

![Rendered image with three galaxies and three stars and no background noise. The PSF size changes for different seeings.\label{fig:psfonly}](psf_variations.png)

In the simplest case, UFig can render an image with a few predefined galaxies and stars without background noise.
An example of such a rendered image is shown in \autoref{fig:psfonly}.
From left to right, you see the same objects with different seeing conditions, which change the size of the PSF.
The PSF is modelled as a mixture of one or two Moffat profiles $I_i(r)$ given by
\begin{equation}
    \begin{aligned}
        I_i(r) &= I_{0,i}\left(1 + \left(\frac{r}{\alpha_i}\right)^2\right)^{-\beta_i},
    \end{aligned}
\end{equation}
with a constant base profile across the image.
The ratio of $I_{0,1}$ and $I_{0,2}$ is a free parameter (in the case of a two-component Moffat) and the sum of the two profiles is determined by the number of photons of the object.
The $\beta_i$ parameter is free and $\alpha_i$ is chosen such that the half light radius of the profile is one pixel.
This base profile is then distorted at each position of an object by three transformations accounting for the size of the PSF, the shape of the PSF (ellipticity, skewness, triangularity and kurtosity) and the position of the PSF, see @herbel_psf for more details.
These distortions can be passed as a constant value across the image, as a map with varying values for each pixel or estimated using the CNN presented in @herbel_psf.

\autoref{fig:bkg} shows the same image as in \autoref{fig:psfonly} but with added background noise.
Background noise can be added as a Gaussian with constant mean and standard deviation across the image or as a map with varying mean and standard deviation for each pixel.

![Rendered image with three galaxies and three stars, constant PSF and different background levels. The left panel shows an image with low background noise, the middle panel higher noise and the right panel shows an image where each quarter has a different background noise.\label{fig:bkg}](bkg_variations.png)

Creating a more realistic galaxy catalog can be done by using the GalSBI galaxy population model and the corresponding galaxy sampling plugins of UCat.
An example of rendered images for different bands with galaxies sampled from the GalSBI model presented in @fischbacher is shown in \autoref{fig:galsbi}.

![Rendered images with galaxies sampled from the GalSBI model for different bands\label{fig:galsbi}](galsbi.png)

# Acknowledgements

We acknowledge the use of the following software packages: `numpy` [@numpy], `scipy` [@scipy], `astropy` [@astropy], `healpy` [@healpy], `numba` [@numba], `edelweiss` [@fischbacher], `scikit-learn` [@scikit-learn].
The authors with the equal contribution are listed in inverse order of their main contribution.

# References
