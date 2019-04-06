# CODING-STYLE CHECKS:
# pycodestyle test_consumption.py

import numpy as np
import pytest
import copy
from taxcalc import Policy, Records, Calculator, Consumption


def test_year_consistency():
    assert Consumption.JSON_START_YEAR == Policy.JSON_START_YEAR
    assert Consumption.DEFAULT_NUM_YEARS == Policy.DEFAULT_NUM_YEARS


def test_validity_of_consumption_vars_set():
    assert Consumption.RESPONSE_VARS.issubset(Records.USABLE_READ_VARS)
    useable_vars = set(['housing', 'snap', 'tanf', 'vet', 'wic',
                        'mcare', 'mcaid', 'other'])
    assert Consumption.BENEFIT_VARS.issubset(useable_vars)


def test_update_consumption():
    consump = Consumption()
    consump.update_consumption({})
    consump.update_consumption({2014: {'MPC_e20400': 0.05,
                                       'BEN_mcare_value': 0.75},
                                2015: {'MPC_e20400': 0.06,
                                       'BEN_mcare_value': 0.80}})
    expected_mpc_e20400 = np.full((Consumption.DEFAULT_NUM_YEARS,), 0.06)
    expected_mpc_e20400[0] = 0.0
    expected_mpc_e20400[1] = 0.05
    assert np.allclose(consump._MPC_e20400,
                       expected_mpc_e20400,
                       rtol=0.0)
    assert np.allclose(consump._MPC_e17500,
                       np.zeros((Consumption.DEFAULT_NUM_YEARS,)),
                       rtol=0.0)
    expected_ben_mcare_value = np.full((Consumption.DEFAULT_NUM_YEARS,), 0.80)
    expected_ben_mcare_value[0] = 1.0
    expected_ben_mcare_value[1] = 0.75
    assert np.allclose(consump._BEN_mcare_value,
                       expected_ben_mcare_value,
                       rtol=0.0)
    assert np.allclose(consump._BEN_snap_value,
                       np.ones((Consumption.DEFAULT_NUM_YEARS,)),
                       rtol=0.0)
    consump.set_year(2015)
    assert consump.current_year == 2015
    assert consump.MPC_e20400 == 0.06
    assert consump.MPC_e17500 == 0.0
    assert consump.BEN_mcare_value == 0.80
    assert consump.BEN_snap_value == 1.0


def test_incorrect_update_consumption():
    with pytest.raises(ValueError):
        Consumption().update_consumption([])
    with pytest.raises(ValueError):
        Consumption().update_consumption({'xyz': {'MPC_e17500': 0.2}})
    with pytest.raises(ValueError):
        Consumption().update_consumption({2012: {'MPC_e17500': 0.2}})
    with pytest.raises(ValueError):
        Consumption().update_consumption({2052: {'MPC_e17500': 0.2}})
    with pytest.raises(ValueError):
        Consumption().update_consumption({2014: {'MPC_exxxxx': 0.2}})
    with pytest.raises(ValueError):
        Consumption().update_consumption({2014: {'MPC_e17500': -0.1}})


def test_future_update_consumption():
    consump = Consumption()
    assert consump.current_year == consump.start_year
    assert consump.has_response() is False
    cyr = 2020
    consump.set_year(cyr)
    consump.update_consumption({cyr: {'MPC_e20400': 0.01}})
    assert consump.current_year == cyr
    assert consump.has_response() is True
    consump.set_year(cyr - 1)
    assert consump.has_response() is False
    # test future updates for benefits
    consump_ben = Consumption()
    assert consump_ben.current_year == consump_ben.start_year
    assert consump_ben.has_response() is False
    consump_ben.set_year(cyr)
    consump_ben.update_consumption({cyr: {'BEN_vet_value': 0.95}})
    assert consump_ben.current_year == cyr
    assert consump_ben.has_response() is True
    consump_ben.set_year(cyr - 1)
    assert consump_ben.has_response() is False


def test_consumption_default_data():
    consump = Consumption()
    pdata = consump._vals
    for pname in pdata.keys():
        if pname.startswith('MPC'):
            assert pdata[pname]['value'] == [0.0]
        elif pname.startswith('BEN'):
            assert pdata[pname]['value'] == [1.0]


def test_consumption_response(cps_subsample):
    consump = Consumption()
    mpc = 0.5
    consumption_response = {2013: {'MPC_e20400': mpc}}
    consump.update_consumption(consumption_response)
    # test incorrect call to response method
    with pytest.raises(ValueError):
        consump.response(list(), 1)
    # test correct call to response method
    rec = Records.cps_constructor(data=cps_subsample)
    pre = copy.deepcopy(rec.e20400)
    consump.response(rec, 1.0)
    post = rec.e20400
    actual_diff = post - pre
    expected_diff = np.ones(rec.array_length) * mpc
    assert np.allclose(actual_diff, expected_diff)
    # compute earnings mtr with no consumption response
    rec = Records.cps_constructor(data=cps_subsample)
    ided0 = copy.deepcopy(rec.e20400)
    calc0 = Calculator(policy=Policy(), records=rec, consumption=None)
    (mtr0_ptax, mtr0_itax, _) = calc0.mtr(variable_str='e00200p',
                                          wrt_full_compensation=False)
    assert np.allclose(calc0.array('e20400'), ided0)
    # compute earnings mtr with consumption response
    calc1 = Calculator(policy=Policy(), records=rec, consumption=consump)
    mtr1_ptax, mtr1_itax, _ = calc1.mtr(variable_str='e00200p',
                                        wrt_full_compensation=False)
    assert np.allclose(calc1.array('e20400'), ided0)
    # confirm that payroll mtr values are no different
    assert np.allclose(mtr1_ptax, mtr0_ptax)
    # confirm that all mtr with cons-resp are no greater than without cons-resp
    assert np.all(np.less_equal(np.around(mtr1_itax, decimals=5),
                                np.around(mtr0_itax, decimals=5)))
    # confirm that some mtr with cons-resp are less than without cons-resp
    assert np.any(np.less(mtr1_itax, mtr0_itax))


def test_validate_assump_parameters_errors():
    """
    Check detection of invalid consumption parameter names, types, values.
    """
    con0 = Consumption()
    parm0 = {2020: {'STD': True}}  # invalid name
    with pytest.raises(ValueError):
        con0.update_consumption(parm0)
    con1 = Consumption()
    parm1 = {2020: {'MPC_e17500': False}}
    with pytest.raises(ValueError):
        con1.update_consumption(parm1)
    con2 = Consumption()
    parm2 = {2020: {'MPC_e17500': -0.5}}
    with pytest.raises(ValueError):
        con2.update_consumption(parm2)
    con3 = Consumption()
    parm3 = {2020: {'MPC_e17500': 1.5}}
    with pytest.raises(ValueError):
        con3.update_consumption(parm3)
