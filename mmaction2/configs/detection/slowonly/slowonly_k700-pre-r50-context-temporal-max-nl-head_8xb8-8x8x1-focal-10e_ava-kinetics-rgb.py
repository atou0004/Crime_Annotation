_base_ = ['slowonly_k700-pre-r50_8xb8-8x8x1-10e_ava-kinetics-rgb.py']

model = dict(
    roi_head=dict(
        bbox_roi_extractor=dict(with_global=True, temporal_pool_mode='max'),
        bbox_head=dict(in_channels=4096, mlp_head=True, focal_gamma=1.0)))
