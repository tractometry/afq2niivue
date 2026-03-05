# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "ipyniivue==2.4.4",
#     "ipywidgets==8.1.8",
#     "marimo>=0.20.2",
#     "trx-python==0.3",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import os
    from ipyniivue import NiiVue, ShowRender
    from trx.io import load, save
    import os.path as op


    return NiiVue, ShowRender, load, mo, op


@app.cell
def _(load, op):
    trx = load(op.join("sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography", 
                       "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography.trx"), 
               "same")
    return (trx,)


@app.cell
def _(trx):
    list(trx.groups.keys())
    return


@app.cell
def _(NiiVue, ShowRender):
    nv = NiiVue(
        back_color=(1, 1, 1, 1),
        show_3d_crosshair=True,
        multiplanar_show_render=ShowRender.ALWAYS,
        yoke_3d_to_2d_zoom=True,
    )
    return (nv,)


@app.cell
def _(nv, op):
    nv.load_meshes(op.join("sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography",
                           "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography.trx"))
    return


@app.cell
def _(nv):
    nv.meshes[0].id
    return


@app.cell
def _(nv):
    nv.load_volumes([
        {"path": "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography/sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-masked_T1w.nii.gz"}
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    # Tractography Viewer

    Visualization of white matter fiber bundles from diffusion MRI tractography, overlaid on a T1-weighted anatomical image.
    """)
    return


@app.cell
def _(mo, nv, trx):
    # nv = NiiVue(
    #     back_color=(1, 1, 1, 1),
    #     show_3d_crosshair=True,
    #     multiplanar_show_render=ShowRender.ALWAYS,
    #     yoke_3d_to_2d_zoom=True,
    # )

    # nv.load_volumes([
    #     {"path": "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography/sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-masked_T1w.nii.gz"}
    # ])

    # bundle_dir = "bundles"
    # bundle_files = sorted(
    #     [f for f in os.listdir(bundle_dir) if f.endswith(".trx")])

    # nv.load_meshes([
    #     {"path": f"{bundle_dir}/{f}"} for f in bundle_files
    # ])

    nv.set_clip_plane(-0.2, 0, 120)

    for mesh in nv.meshes:
        nv.set_mesh_property(mesh.id, "visible", False)

    # bundle_names = [f.replace(".trx", "") for f in bundle_files]

    region_buttons = [
        mo.ui.checkbox(
            value=False,
            label=name,
            on_change=lambda checked, i=i: (
                nv.set_mesh_property(nv.meshes[i].id, "visible", checked),
                nv.set_mesh_property(
                    nv.meshes[i].id, "fiber_radius", 0.5 if checked else 0.0),
            ),
        )
        for i, name in enumerate(list(trx.groups.keys()))
    ]

    mo.vstack([
        mo.hstack([]),
        nv,
        mo.md("**Regions:**"),
        mo.hstack(region_buttons, wrap=True),
    ])
    return


@app.cell
def _(nv):
    nv.xwx(mesh_id=0, attribute="fiber_color", value=[])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
