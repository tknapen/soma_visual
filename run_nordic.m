cd('/Users/knapen/projects/soma_visual/data/sourcedata/sub-06/func');

ARG.DIROUT = '/Users/knapen/projects/soma_visual/data/sourcedata_nordic/sub-06/func/';
ARG.phase_filter_width=10;
ARG.temporal_phase=1;

conditions = ["VM" "VO" "AM"];

for c = 1:6
    for i = 1:3
        fn_out = strcat("sub-06_acq-mag_task-", conditions(i), "_run-", int2str(c) , "_bold");
        fn_magn_in = strcat("sub-06_acq-mag_task-", conditions(i), "_run-", int2str(c) , "_bold.nii.gz");
        fn_phase_in = strcat("sub-06_acq-phase_task-", conditions(i), "_run-", int2str(c) , "_bold.nii.gz");
        
        NIFTI_NORDIC(fn_magn_in,fn_phase_in,fn_out,ARG)
    end
end