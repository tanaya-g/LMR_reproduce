import cfr
import numpy as np

def main():
    job = cfr.ReconJob()
    job.load_proxydb('PAGES2kv2')

    # load model prior
    job.load_clim(
        tag='prior',
        
        path_dict= {
        'tas': './prev_data/ccsm4_last_millenium/tas_sfc_Amon_CCSM4_past1000_085001-185012.nc',
        'pr': './prev_data/ccsm4_last_millenium/pr_sfc_Amon_CCSM4_past1000_085001-185012.nc'
        },
        anom_period=[850,1850],  # Tardif 2019 uses entire interval
        load=True,  
        verbose=True,
    )

    # load instrumental observations
    job.load_clim(
        tag='obs',
        path_dict={
            'pr': './prev_data/GPCC_precip.mon.flux.1x1.v6.nc',  
            'tas': 'gistemp1200_ERSSTv4'
        },
        rename_dict={'pr': 'precip','tas': 'tempanomaly'},
        anom_period=[1951, 1980], 
        load=True,
    )

    # calibrate psms
    ptype_psm_dict = {
        'tree.TRW': 'Bilinear',
        'tree.MXD': 'Linear',
        'coral.d18O': 'Linear',
        'coral.SrCa': 'Linear',
        'ice.d18O': 'Linear',
        'lake.varve_thickness': 'Linear',
    }

    # target variables
    ptype_clim_dict = {
        'tree.TRW': ['tas', 'pr'],
        'tree.MXD': ['tas'],
        'coral.d18O': ['tas'],
        'coral.SrCa': ['tas'],
        'ice.d18O': ['tas'],
        'lake.varve_thickness': ['tas'],
    }

    # Seasonality for each proxy type
    ptype_season_dict = {
        'tree.TRW': [  # expert curated pool of possible growing seasons
            [1,2,3,4,5,6,7,8,9,10,11,12],
            [6,7,8],
            [3,4,5,6,7,8],
            [6,7,8,9,10,11],
            [-12,1,2],
            [-9,-10,-11,-12,1,2],
            [-12,1,2,3,4,5],
        ],
        'tree.MXD': [  # expert curated pool of possible growing seasons
            #[1,2,3,4,5,6,7,8,9,10,11,12],
            [6,7,8],
            [3,4,5,6,7,8],
            [6,7,8,9,10,11],
            [-12,1,2],
            [-9,-10,-11,-12,1,2],
            [-12,1,2,3,4,5],
        ],
        'coral.d18O': list(range(1, 13)),            # annual
        'coral.SrCa': list(range(1, 13)),            # annual
        'ice.d18O': list(range(1, 13)),              # annual
        'lake.varve_thickness': list(range(1, 13)),  # annual
    }

    job.calib_psms(
        ptype_psm_dict=ptype_psm_dict,
        ptype_season_dict=ptype_season_dict,
        ptype_clim_dict=ptype_clim_dict,
        nobs_lb = 25, # as used in Tardif 2019
        verbose=True,
    )

    job.forward_psms(verbose=True)

    # annualize and regrid
    job.annualize_clim(tag='prior', verbose=True, months=list(range(1, 13)))
    job.regrid_clim(tag='prior', nlat=42, nlon=63, verbose=True)

    job.save('./cases/lmr_reproduce_pda', verbose=True)

    job.run_da_mc(
        save_dirpath='./recons/lmr_reproduce_pda',
        recon_seeds=list(range(1, 51)),  # as an example here
        recon_vars=['tas','pr'],  # add 'pr' to reconstruct both the tas and pr fields
        recon_period=[1, 2000],
        verbose=True,
    )

if __name__ == '__main__':
    main()