"""A minimal vasprun.xml with the elements VASP writes and the convergence check reads."""


def _vasprun(n_scsteps, *, nelm=60, nsw=0, ibrion=-1, n_ionic=1, incar_extra="", energy=-71.78294695):
    """A minimal vasprun.xml with the elements VASP writes and the validator reads."""
    scstep = '  <scstep><energy><i name="e_fr_energy"> -71.7 </i></energy></scstep>\n'
    calc = (
        " <calculation>\n"
        + scstep * n_scsteps
        + f'  <energy><i name="e_fr_energy"> {energy} </i><i name="e_0_energy"> {energy} </i></energy>\n'
        " </calculation>\n"
    )
    return (
        '<?xml version="1.0" encoding="ISO-8859-1"?>\n<modeling>\n'
        f' <incar>\n  <i type="int" name="IBRION"> {ibrion} </i>\n{incar_extra} </incar>\n'
        " <parameters>\n"
        f'  <separator name="electronic">\n   <i type="int" name="NELM"> {nelm} </i>\n  </separator>\n'
        f'  <separator name="ionic">\n   <i type="int" name="NSW"> {nsw} </i>\n'
        f'   <i type="int" name="IBRION"> {ibrion} </i>\n  </separator>\n'
        '  <separator name="response functions">\n   <i type="int" name="NELM"> 1 </i>\n  </separator>\n'
        " </parameters>\n" + calc * n_ionic + "</modeling>\n"
    )
