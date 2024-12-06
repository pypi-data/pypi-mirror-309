Quick start
***********

The fastest way to get started is to look at the examples/ directory, which
has examples on how to compute transit/eclipse depths from planetary parameters, and
on how to retrieve planetary parameters from transit/eclipse depths.  This page is
a short summary of the more detailed examples.

To compute transit depths, look at transit_depth_example.py, then go to
:class:`.TransitDepthCalculator` for more info.  In short::

  from platon.transit_depth_calculator import TransitDepthCalculator
  from platon.constants import M_jup, R_jup, R_sun

  # All inputs and outputs for PLATON are in SI
  
  Rs = 1.16 * R_sun
  Mp = 0.73 * M_jup
  Rp = 1.40 * R_jup
  T = 1200

  # The initializer loads all data files.  Create a TransitDepthCalculator
  # object and hold on to it
  calculator = TransitDepthCalculator()

  # compute_depths is fast once data files are loaded
  wavelengths, depths, info_dict = calculator.compute_depths(Rs, Mp, Rp, T, logZ=0, CO_ratio=0.53, full_output=True)

You can adjust a variety of parameters, including the metallicity (Z) and C/O
ratio. By default, logZ = 0 and C/O = 0.53. Any other value for
logZ and C/O in the range -2 < logZ < 3 and 0.001 < C/O < 2 can also be used.
full_output=True indicates you'd like extra information about the atmosphere,
which is returned in info_dict.  info_dict includes parameters like the
temperatures, pressures, radii, abundances, and molecular weights of each
atmospheric layer, and the line of sight optical depth (tau_los) through each
layer.

You can also specify custom abundances, albeit in a somewhat hacky way::
  
  from platon.abundance_getter import AbundanceGetter
  abundances = AbundanceGetter().get(0, 0.5) #logZ=0, C/O=0.5 equilibrium abundances
  abundances["H2O"] *= 0
  abundances["H2O"] += 1e-4 #10^-4 VMR at all temperatures and pressures

  abundances["CO2"] *= 0
  abundances["CO2"] += 1e-5
  
  calculator.compute_depths(Rs, Mp, Rp, T, logZ=None, CO_ratio=None,
                            custom_abundances=abundances)
			    
To retrieve atmospheric parameters, look at retrieve_dynesty.py, retrieve_multinest.py, retrieve_emcee.py, or retrieve_eclipses.py, then go to
:class:`.CombinedRetriever` for more info.  In short, for an equilibrium retrieval::

  from platon.fit_info import FitInfo
  from platon.combined_retriever import CombinedRetriever

  retriever = CombinedRetriever()
  fit_info = retriever.get_default_fit_info(Rs, Mp, Rp, T, logZ=0, CO_ratio=0.5, T_star=6100)

  # Decide what you want to fit for, and add those parameters to fit_info

  # Fit for the stellar radius and planetary mass using Gaussian priors.  This
  # is a way to account for the uncertainties in the published values
  fit_info.add_gaussian_fit_param('Rs', 0.02*R_sun)
  fit_info.add_gaussian_fit_param('Mp', 0.04*M_jup)

  # Fit for other parameters using uniform priors
  fit_info.add_uniform_fit_param('R', 0.9*R_guess, 1.1*R_guess)
  fit_info.add_uniform_fit_param('T', 0.5*T_guess, 1.5*T_guess)
  fit_info.add_uniform_fit_param("log_scatt_factor", 0, 1)
  fit_info.add_uniform_fit_param("logZ", -1, 3)
  fit_info.add_uniform_fit_param("CO_ratio", 0.2, 2)
  fit_info.add_uniform_fit_param("log_cloudtop_P", -0.99, 5)
  fit_info.add_uniform_fit_param("error_multiple", 0.5, 5)
  
  # Run nested sampling. You can replace run_dynesty with run_pymultinest,
  # which is sometimes much faster and more robust
  result = retriever.run_dynesty(
	 bins, depths, errors, #transit bins, depths, errors
         None, None, None, #eclipse bins, depths, errors
	 fit_info, plot_best=True)

Here, `bins` is a N x 2 array representing the start and end wavelengths of the
bins, in metres; `depths` is a list of N transit depths; and `errors` is a list
of N errors on those transit depths.  `plot_best=True` indicates that the best
fit solution should be plotted, along with the measured transit depths and
their errors.

The example above retrieves the planetary radius (at a reference pressure
of 10^5 Pa), the temperature of the isothermal atmosphere, and the
metallicity.  Other parameters you can retrieve for include the stellar radius,
the planetary mass, C/O ratio,
the cloudtop pressure, the scattering factor, the scattering slope,
and the error multiple--which multiplies all errors by a constant.  We recommend
either fixing the stellar radius and planetary mass to the measured values, or
setting Gaussian priors on them to account for measurement errors.

To do a free retrieval, set logZ=None, CO_ratio=None, and fit_vmr=True in get_default_fit_info, and add::

  fit_info.add_gases_vmr(["CH4", "CO2", "CO", "H2O", "H2S", "H2-He"], 10**-12, 10**-2)

This fits the log VMR of the gases CH4, CO2, CO, H2O, and H2S, with a H2/He mixture
as the background gas.  The VMRs of the non-background gases are given log-uniform
priors between 1e-12 and 1e-2.  Alternatively, you can do a free retrieval with
centered-log-ratio (CLR) priors::

  fit_info.add_gases_vmr(["CH4", "CO2", "CO", "H2O", "H2S"])

With a CLR prior, all gases are treated equally, and there is no pre-defined background gas.

Once you get the `result` object, you should store the object, in addition
to plotting the posterior distribution and the best fit::

  with open("example_retrieval_result.pkl", "wb") as f:
     pickle.dump(result, f)

  from platon.plotter import Plotter
  plotter = Plotter()
  plotter.plot_retrieval_transit_spectrum(result, prefix="best_fit")
  plotter.plot_retrieval_corner(result, filename="dynesty_corner.png")

If you prefer using MCMC instead of Nested Sampling in your retrieval, you can
use the run_emcee method instead of the run_dynesty method. Do note that
Nested Sampling is recommended, as it is not trivial to deal with multi-modal
posteriors or to check for convergence with emcee::

  result = retriever.run_emcee(bins, depths, errors, fit_info)

For MCMC, the number of walkers and iterations/steps can also be specified. The
`result` object returned by run_emcee is different from that returned
by run_dynesty, but the same plotter can be used.

After a retrieval, PLATON automatically computes the Pareto importance sampling leave-one-out cross-validation score (PSIS-LOO), first used in an exoplanet context by `Welbanks et al 2023 <https://ui.adsabs.harvard.edu/abs/2023AJ....165..112W/abstract>`_.  The values are stored in the retrieval pickle file as "loos" (also see "loo_total" and "loo_ks").  
