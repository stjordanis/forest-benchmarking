import numpy as np
from numpy import pi
from forest.benchmarking.qubit_spectroscopy import (generate_rabi_experiments,
                                                    acquire_qubit_spectroscopy_data,
                                                    fit_rabi_results,
                                                    get_stats_by_qubit)


def test_rabi_flop(qvm):
    qubits = [0]
    num_shots = 100
    qvm.qam.random_seed = 1
    angles = np.linspace(0, 2 * pi, 15)
    rabi_expts = generate_rabi_experiments(qubits, angles)
    results = acquire_qubit_spectroscopy_data(qvm, rabi_expts, num_shots)
    stats = get_stats_by_qubit(results)[qubits[0]]

    fit = fit_rabi_results(angles, stats['expectation'], stats['std_err'])

    freq = fit.params['frequency'].value
    freq_err = fit.params['frequency'].stderr

    assert np.isclose(freq, 1, atol=2 * freq_err)

    amplitude = fit.params['amplitude'].value
    amplitude_err = fit.params['amplitude'].stderr

    assert np.isclose(amplitude, -.5, atol=2 * amplitude_err)

    baseline = fit.params['baseline'].value
    baseline_err = fit.params['baseline'].stderr

    assert np.isclose(baseline, .5, atol=2 * baseline_err)
