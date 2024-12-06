#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""adparallel.py

This file is part of PAutoDock.
Copyright (C) 2020 Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
PAutoDock is distributed under GPLv3 license.
To know more in detail how the license work,
please read the file "LICENSE" or
go to "http://www.gnu.org/licenses/gpl-3.0.en.html"


Provides the basic code to run autodock in parallel on a machine.

"""

import logging
import math
import multiprocessing
import os
import shutil
import tempfile
from pathlib import Path

from pautodock import molop, multimol2op
from pautodock.fileutils import get_bin_path
from pautodock.mgltoolsinstall import install_mgltools


class ADParallel(object):
    def __init__(self, receptor, ligand, db, wpath):
        try:
            self.atdpath = get_bin_path("autodock")
        except ValueError:
            self.atdpath = None
        try:
            self.vinapath = get_bin_path("vina")
        except ValueError:
            self.vinapath = None

        if not self.atdpath and not self.vinapath:
            msg = "Error!! autodock and vina are not installed!\n"
            msg += "Unable to run any calculation."
            raise ValueError(msg)

        self.mglpath = Path(f"{Path.home()}/.pautodock/MGLTools")
        if not self.mglpath.exists():
            install_mgltools(f"{Path.home()}/.pautodock")
        self.receptor = receptor
        self.ligand = ligand
        self.db = db
        self.wpath = wpath
        self.results = []
        self.cx = 0.0
        self.cy = 0.0
        self.cz = 0.0
        self.gsize_x = 30
        self.gsize_y = 30
        self.gsize_z = 30
        self.speed = "slow"
        self.atd = True
        self.vina = True
        self.exhaustiveness = 32
        self.num_modes = 18

    def read_atom_types(self, rec_mol):
        """
        Read atom types in pdb and return in a list
        """
        atlst = []
        f = open(rec_mol, "r")
        for line in f:
            if "ATOM" in line:
                at = line.strip().split(" ")[-1]
                if at in atlst:
                    continue
                else:
                    if len(at) > 0:
                        atlst.append(at)
                    else:
                        continue
        f.close()
        atlst = list(set(atlst))
        atypes_str = "%s" % atlst[0]
        for i in range(1, len(atlst)):
            atypes_str += " %s" % atlst[i]
        return atypes_str, atlst

    def write_autodock_param_files(self, path, rec_pdbqt, mol_pdbqt, cc):
        path_ = Path(path).absolute()
        rat_str, _ = self.read_atom_types(rec_pdbqt)
        lat_str, lat_lst = self.read_atom_types(path + "/" + mol_pdbqt)
        # write the GPF
        f = open(path + "/grid.gpf", "w")
        f.write(
            "npts %d %d %d # num.grid points in xyz\n"
            % (self.gsize_x, self.gsize_y, self.gsize_z)
        )
        f.write("gridfld %s/receptor_model.maps.fld     # grid_data_file\n" % (path_))
        f.write("spacing 0.33 # spacing(A)\n")
        f.write("receptor_types %s # receptor atom types\n" % (rat_str))
        f.write("ligand_types %s # ligand atom types\n" % (lat_str))
        f.write("receptor %s    # macromolecule\n" % (rec_pdbqt))
        f.write(
            "gridcenter %.3f %.3f %.3f       # xyz-coordinates or auto\n"
            % (cc[0], cc[1], cc[2])
        )
        f.write("smooth 0.5  # store minimum energy w/in rad(A)\n")
        for at in lat_lst:
            f.write(
                "map %s/receptor_model.%s.map # atom-specific aff. map\n" % (path_, at)
            )
        f.write("elecmap %s/receptor_model.e.map # El. Pot potential map\n" % (path_))
        f.write("dsolvmap %s/receptor_model.d.map # desolv. potential map\n" % (path_))
        f.write("dielectric -0.1465 # <0, AD4 dist-dep.diel;>0, constant\n")
        f.close()

        # Write autodock file
        f = open(path + "/ind.dpf", "w")
        f.write("autodock_parameter_version 4.2")
        f.write("# used by autodock to validate parameter set\n")
        f.write("outlev 1 # diagnostic output level\n")
        f.write("intelec # calculate internal electrostatics\n")
        f.write("seed time pid # seeds for random generator\n")
        f.write("ligand_types %s # atoms types in ligand\n" % (lat_str))
        f.write("fld %s/receptor_model.maps.fld      # grid_data_file\n" % (path_))
        for at in lat_lst:
            f.write(
                "map %s/receptor_model.%s.map # atom-specific aff. map\n" % (path_, at)
            )
        f.write("elecmap %s/receptor_model.e.map    # electrostatics map\n" % (path_))
        f.write("desolvmap %s/receptor_model.d.map   # desolvation map\n" % (path_))
        f.write("move %s/%s                    # small molecule\n" % (path_, mol_pdbqt))
        f.write(
            "about %.4f %.4f %.4f       # small molecule center\n"
            % (cc[0], cc[1], cc[2])
        )
        f.write("tran0 %.4f %.4f %.4f " % (cc[0], cc[1], cc[2]))
        f.write("# initial coordinates/A or random\n")
        f.write("quaternion0 random ")
        f.write("# initial orientation\n")
        f.write("dihe0 random ")
        f.write("# initial dihedrals (relative) or random\n")
        f.write("torsdof 5 ")
        f.write("# torsional degrees of freedom\n")
        f.write("rmstol 2.0  # cluster_tolerance/A\n")
        f.write("extnrg 1000.0  # external grid energy\n")
        f.write("e0max 0.0 10000 ")
        f.write("# max initial energy; max number of retries\n")
        f.write("ga_pop_size 150 ")
        f.write("# number of individuals in population\n")
        if self.speed == "slow":
            f.write("ga_num_evals 25000000 ")
        elif self.speed == "medium":
            f.write("ga_num_evals 2500000 ")
        else:
            f.write("ga_num_evals 250000 ")
        f.write("               # maximum number of energy evaluations\n")
        f.write("ga_num_generations 27000 ")
        f.write("# maximum number of generations\n")
        f.write("ga_elitism 1 ")
        f.write("# number of top individuals to survive to next generation\n")
        f.write("ga_mutation_rate 0.02 # rate of gene mutation\n")
        f.write("ga_crossover_rate 0.8 # rate of crossover\n")
        f.write("ga_window_size 10 # \n")
        f.write("ga_cauchy_alpha 0.0 ")
        f.write("# Alpha parameter of Cauchy distribution\n")
        f.write("ga_cauchy_beta 1.0 ")
        f.write("# Beta parameter Cauchy distribution\n")
        f.write("set_ga")
        f.write(" # set the above parameters for GA or LGA\n")
        f.write("sw_max_its 300")
        f.write("# iterations of Solis & Wets local search\n")
        f.write("sw_max_succ 4 ")
        f.write(" # consecutive successes before changing rho\n")
        f.write("sw_max_fail 4 ")
        f.write(" # consecutive failures before changing rho\n")
        f.write("sw_rho 1.0 ")
        f.write("# size of local search space to sample\n")
        f.write("sw_lb_rho 0.01                       # lower bound on rho\n")
        f.write("ls_search_freq 0.06 ")
        f.write("# probability of performing local search on individual\n")
        f.write("set_psw1 ")
        f.write("# set the above pseudo-Solis & Wets parameters\n")
        f.write("unbound_model bound ")
        f.write("# state of unbound ligand\n")
        f.write("ga_run 10 ")
        f.write("# do this many hybrid GA-LS runs\n")
        f.write("analysis ")
        f.write("# perform a ranked cluster analysis\n")
        f.close()
        grid_path = Path(path + "/grid.gpf").absolute()
        ind_path = Path(path + "/ind.dpf").absolute()
        return grid_path, ind_path

    def write_vina_param_files(self, path, cc, ss):
        vina_conf_path = Path(path) / "vina_conf.txt"
        with vina_conf_path.open("w", encoding="utf8") as f:
            f.write(f"center_x = {cc[0]:.4f}\n")
            f.write(f"center_y = {cc[1]:.4f}\n")
            f.write(f"center_z = {cc[2]:.4f}\n")
            f.write(f"size_x = {ss[0]}\n")
            f.write(f"size_y = {ss[1]}\n")
            f.write(f"size_z = {ss[2]}\n")
            f.write(f"num_modes = {self.num_modes}\n")
            f.write(f"exhaustiveness = {self.exhaustiveness}\n")
        return vina_conf_path.resolve()

    def RunAutoGrid(self, cmd):
        atg_path = str(Path("%s/autogrid4" % (self.atdpath)).absolute())
        return os.system("%s %s" % (atg_path, cmd))

    def RunAutoDock(self, cmd):
        atd_path = str(Path("%s/autodock4" % (self.atdpath)).absolute())
        return os.system("%s %s" % (atd_path, cmd))

    def RunVina(self, cmd):
        vina_path = str(Path("%s/vina" % (self.vinapath)).absolute())
        return os.system("%s %s" % (vina_path, cmd))

    def ReadOutput(self, ofile):
        r = []
        header = []
        benergy = []
        c_rmsd = []
        r_rmsd = []
        f = open(str(Path(ofile).absolute()), "r")
        for line in f:
            if "Partition function, Q =" in line:
                header.append("Part. Func.")
                r.append(molop.nsplit(line.strip(), " ")[4])
            elif "Free energy,        A ~" in line:
                r.append(molop.nsplit(line.strip(), " ")[4])
                header.append("Free Energy")
            elif "Internal energy,    U =" in line:
                header.append("Internal Energy")
                r.append(molop.nsplit(line.strip(), " ")[4])
            elif "Entropy,            S =" in line:
                header.append("Entropy")
                r.append(molop.nsplit(line.strip(), " ")[3])
            elif "RANKING" in line:
                v = molop.nsplit(line.strip(), " ")
                benergy.append(float(v[3]))
                c_rmsd.append(float(v[4]))
                r_rmsd.append(float(v[5]))
        f.close()
        header.append("Binding Energy Average")
        r.append(round(sum(benergy) / float(len(benergy)), 3))
        header.append("Cluster RMSD Average")
        r.append(round(sum(c_rmsd) / float(len(c_rmsd)), 3))
        header.append("Ref. RMSD Average")
        r.append(round(sum(r_rmsd) / float(len(r_rmsd)), 3))
        return header, r

    def LigandPosesBaricentreDistance(self, dock_pdbqt: str) -> float:
        """
        Calculate the distance between the ligand and docking pose baricentres.
        """
        poses_cc = molop.get_mol_baricentre(dock_pdbqt)
        if int(self.cx) == 0:
            self.cx, self.cy, self.cz = molop.get_mol_baricentre(self.ligand)
        return math.sqrt(
            (self.cx - poses_cc[0]) ** 2
            + (self.cy - poses_cc[1]) ** 2
            + (self.cz - poses_cc[2]) ** 2
        )

    def read_vina_output(self, ofile):
        benergy = []
        f = open(str(Path(ofile).absolute()), "r")
        getres = False
        for line in f:
            if getres:
                # Filter double outputs
                if "Writing output ... done." in line or "AutoDock Vina" in line:
                    getres = False
                else:
                    try:
                        v = molop.nsplit(line.strip(), " ")
                        benergy.append(float(v[1]))
                    except ValueError as err:
                        logging.error("Error with file %s - %s" % (ofile, err))
            else:
                if "-----+------------+----------+----------" in line:
                    getres = True
                else:
                    continue

        f.close()
        if len(benergy) > 0:
            return (
                round(sum(benergy) / float(len(benergy)), 3),
                min(benergy),
                max(benergy),
            )
        else:
            return 9999.0, 9999.0, 9999.0

    def gen_vs_output(self, vinalogout, dpfout, mnames, otab):
        """
        Collect vina results
        """
        # Collect the vina results
        vbind = []
        for i, vout in enumerate(vinalogout):
            avg_b, min_b, max_b = self.read_vina_output(vout)
            try:
                dock_poses = (
                    f"{Path(vout).parent.absolute()}/dock_confs_{mnames[i]}.pdbqt"
                )
                lp_dst = self.LigandPosesBaricentreDistance(dock_poses)
            except FileNotFoundError as err:
                logging.error("%s not found", err)
                lp_dst = 9999.0
            vbind.append([avg_b, min_b, max_b, lp_dst])
        # Collect results
        fo = open(otab, "w")
        firstline = True
        for i in range(len(mnames)):
            h = []
            r = []
            if len(dpfout) > 0:
                if Path(dpfout[i]).is_file():
                    h, r = self.ReadOutput(dpfout[i])
            if firstline:
                firstline = False
                fo.write("Molname;")
                for j in range(len(h)):
                    fo.write("%s;" % (h[j]))
                fo.write("Avg. vina Binding Energy;")
                fo.write("Min vina Binding Energy;Max vina Binding Energy;")
                fo.write("Template-Ligand Baricenter Distance (docking pose check)\n")
            fo.write("%s;" % (mnames[i]))
            for j in range(len(r)):
                fo.write("%s;" % (r[j]))
            fo.write(
                "%f;%f;%f;%f\n" % (vbind[i][0], vbind[i][1], vbind[i][2], vbind[i][3])
            )
        fo.close()

    def make_vina_cmd(
        self, vconf_path, rec_pdbqt, mol_pdbqt, mpath, molname, vinalogout
    ) -> str:
        vc = f'--config "{vconf_path}"'
        vc += f' --receptor "{rec_pdbqt}"'
        vc += f' --ligand "{mol_pdbqt}"'
        vc += f' --out "{mpath}/dock_confs_{molname}.pdbqt" >> {vinalogout}'
        return vc

    def virtual_screening(self, otab):
        # Prepare the receptor
        rec = molop.Receptor(self.receptor, self.mglpath)
        rec_pdbqt = rec.topdbqt()
        if self.ligand is not None:
            self.cx, self.cy, self.cz = molop.get_mol_baricentre(self.ligand)
        # Prepare the database split multi mol2
        tmppath = tempfile.mkdtemp()
        mol2lst = multimol2op.split_mol2(self.db, tmppath)
        agcmdlst = []
        adcmdlst = []
        vinacmdlst = []
        vinalogout = []
        dpfout = []
        mnames = []
        # Create a directory with the name of the mol2 molecule
        # and copy the receptor and itself
        for mol2 in mol2lst:
            molname_ext = str(Path(mol2).resolve().name)
            molname = molname_ext.replace(".mol2", "")
            mnames.append(molname)
            mpath = str(Path(self.wpath + "/" + molname).absolute())
            if not Path(f"{mpath}/dock_confs_{molname}.pdbqt").exists():
                if not Path(mpath).exists():
                    os.makedirs(mpath)
                if not Path(mpath + "/" + molname_ext).exists():
                    shutil.move(str(Path(mol2).resolve()), mpath)

                mol = molop.Molecule(
                    str(Path(mpath + "/" + molname_ext).absolute()), self.mglpath
                )
                mol_pdbqt = mol.topdbqt([self.cx, self.cy, self.cz])
                mol_pdbqt_name = str(Path(mol_pdbqt).resolve().name)
                if self.atd:
                    gpf_path, dpf_path = self.write_autodock_param_files(
                        mpath, rec_pdbqt, mol_pdbqt_name, [self.cx, self.cy, self.cz]
                    )
                    first_arg = str(gpf_path)
                    second_arg = str(gpf_path).replace(".gpf", "")
                    ag = f'-p "{first_arg}" -l "{second_arg}.glg"'
                    agcmdlst.append(ag)
                    dpfout.append(str(dpf_path).replace(".dpf", ".dlg"))
                    ad = f'-p "{str(dpf_path)}" -l "{dpfout[-1]}"'
                    adcmdlst.append(ad)

                if self.vina:
                    vinalogout.append(f"{mpath}/vina_log.txt")
                    # If the log and the docking pose extists then
                    # there is no need to run the calculation
                    vconf_path = self.write_vina_param_files(
                        mpath,
                        [self.cx, self.cy, self.cz],
                        [self.gsize_x, self.gsize_y, self.gsize_z],
                    )
                    vinacmdlst.append(
                        self.make_vina_cmd(
                            vconf_path,
                            rec_pdbqt,
                            mol_pdbqt,
                            mpath,
                            molname,
                            vinalogout[-1],
                        )
                    )
            else:
                vinalogout.append(f"{mpath}/vina_log.txt")
        shutil.rmtree(tmppath)
        ncpu = multiprocessing.cpu_count()
        if self.atd:
            # Run AutoGrid
            pool = multiprocessing.Pool(ncpu)
            pool.map(self.RunAutoGrid, agcmdlst)
            # RunAutodock
            pool = multiprocessing.Pool(ncpu)
            pool.map(self.RunAutoDock, adcmdlst)

        if self.vina:
            # RunVina
            pool = multiprocessing.Pool(ncpu)
            pool.map(self.RunVina, vinacmdlst)

        # Write the output table
        self.gen_vs_output(vinalogout, dpfout, mnames, otab)
