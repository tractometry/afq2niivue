# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "ipyniivue==2.4.4",
#     "ipywidgets==8.1.8",
#     "marimo>=0.20.2",
# ]
# ///

import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import zipfile
    import json
    import numpy as np
    import io
    from ipyniivue import NiiVue, ShowRender

    return NiiVue, ShowRender, io, json, mo, np, zipfile


@app.cell
def _(mo):
    mo.md(
        "# Tractography Viewer\n\n"
        "Visualization of white matter fiber bundles from diffusion MRI tractography, overlaid on a T1-weighted anatomical image.\n\n"
        "White matter tractography is a technique used to reconstruct the neural pathways in the brain from diffusion MRI data. Each fiber bundle represents a group of axons connecting different brain regions. This notebook allows you to interactively explore individual bundles from a [TRX](https://github.com/tee-ar-ex/trx-python) tractography file, selecting regions to visualize one at a time.\n\n"
        "This notebook builds on the [NiiVue marimo notebooks](https://github.com/niivue/marimo-notebooks) by Chris Rorden, which demonstrate the use of [NiiVue](https://github.com/niivue/niivue) for neuroimaging visualization in Marimo. The viewer is powered by [ipyniivue](https://github.com/niivue/ipyniivue), the Python wrapper for NiiVue."
    )
    return


@app.cell
def _(mo):
    trx_browser = mo.ui.file_browser(
        initial_path=".",
        filetypes=[".trx"],
        label="Select TRX file (.trx)",
        multiple=False,
    )
    trx_browser
    return trx_browser,


@app.cell
def _(NiiVue, ShowRender):
    nv = NiiVue(
        back_color=(1, 1, 1, 1),
        show_3d_crosshair=True,
        multiplanar_show_render=ShowRender.ALWAYS,
        yoke_3d_to_2d_zoom=True,
    )

    nv.load_volumes([
        {"path": "sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-bundles_tractography/sub-NDARAA948VFH_ses-HBNsiteRU_acq-64dir_desc-masked_T1w.nii.gz"}
    ])

    nv.set_clip_plane(-0.2, 0, 120)

    nv
    return nv,


@app.cell
def _(io, json, mo, np, nv, zipfile, trx_browser):
    mo.stop(
        not trx_browser.value,
        mo.md("**Select a TRX file above to load bundles.**")
    )

    final_trx = str(trx_browser.path())

    with zipfile.ZipFile(final_trx, "r") as z:
        header = json.loads(z.read("header.json"))
        positions = np.frombuffer(
            z.read("positions.3.float16"), dtype=np.float16).reshape(-1, 3)
        offsets = np.frombuffer(z.read("offsets.uint32"), dtype=np.uint32)
        group_files = sorted([
            f for f in z.namelist()
            if f.startswith("groups/") and f != "groups/" and not f.endswith("/")
        ])
        groups = {}
        for gf in group_files:
            name = gf.replace("groups/", "").rsplit(".", 1)[0]
            groups[name] = np.frombuffer(z.read(gf), dtype=np.uint32)

    all_offsets = np.append(offsets, positions.shape[0]).astype(np.int64)
    group_names = list(groups.keys())

    def extract_bundle_trx(group_name):
        indices = groups[group_name]
        new_positions = []
        new_offsets = []
        vertex_count = 0
        for idx in indices:
            start = int(all_offsets[idx])
            end = int(all_offsets[idx + 1])
            pts = positions[start:end]
            new_positions.append(pts)
            new_offsets.append(vertex_count)
            vertex_count += len(pts)

        new_positions = np.vstack(new_positions).astype(np.float16)
        new_offsets = np.array(new_offsets, dtype=np.uint64)

        new_header = {
            "DIMENSIONS": header["DIMENSIONS"],
            "VOXEL_TO_RASMM": header["VOXEL_TO_RASMM"],
            "NB_STREAMLINES": int(len(new_offsets)),
            "NB_VERTICES": int(vertex_count),
        }

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_STORED) as out:
            out.writestr("header.json", json.dumps(new_header))
            out.writestr("positions.3.float16", new_positions.tobytes())
            out.writestr("offsets.uint64", new_offsets.tobytes())
        return buf.getvalue()

    all_bundles = []
    for name in group_names:
        bundle_data = extract_bundle_trx(name)
        all_bundles.append({"data": bundle_data, "name": f"{name}.trx"})

    nv.load_meshes(all_bundles)

    for mesh in nv.meshes:
        nv.set_mesh_property(mesh.id, "visible", False)

    region_checkboxes = [
        mo.ui.checkbox(
            value=False,
            label=name,
            on_change=lambda checked, i=i: (
                nv.set_mesh_property(nv.meshes[i].id, "visible", checked),
                nv.set_mesh_property(
                    nv.meshes[i].id, "fiber_radius", 0.5 if checked else 0.0),
            ),
        )
        for i, name in enumerate(group_names)
    ]

    mo.vstack([
        mo.md("**Regions:**"),
        mo.hstack(region_checkboxes, wrap=True),
    ])
    return


if __name__ == "__main__":
    app.run()
