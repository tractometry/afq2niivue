import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from ipyniivue import NiiVue, ShowRender
    return NiiVue, ShowRender, mo


@app.cell
def _(mo):
    mo.md("""
    # Tractography Viewer

    Visualization of white matter fiber bundles from diffusion MRI tractography, overlaid on a T1-weighted anatomical image.
    """)
    return


@app.cell
def _(NiiVue, ShowRender, mo):
    nv = NiiVue(
        back_color=(1, 1, 1, 1),
        show_3d_crosshair=True,
        multiplanar_show_render=ShowRender.ALWAYS,
    )

    nv.load_volumes([
        {"path": "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography/sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-masked_T1w.nii.gz"}
    ])

    nv.load_meshes([
        {"path": "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography/sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography.trx"}
    ])

    slider_radius = mo.ui.slider(
        start=0,
        stop=1.0,
        step=0.1,
        value=0.5,
        show_value=True,
        label="Fiber Radius",
        on_change=lambda v: setattr(nv.meshes[0], "fiber_radius", v),
    )

    mo.vstack([
        mo.hstack([slider_radius]),
        nv,
    ])
    return


if __name__ == "__main__":
    app.run()
