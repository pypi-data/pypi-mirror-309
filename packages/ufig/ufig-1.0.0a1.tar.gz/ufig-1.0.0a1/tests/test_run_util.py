# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Tue Aug 13 2024


from ufig import run_util


def test_run_util():
    run_util.run_ufig_from_config("ufig.config.test_config")
