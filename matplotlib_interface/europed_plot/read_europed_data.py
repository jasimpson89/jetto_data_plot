import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from dataclasses import dataclass


@dataclass
class CriticalProfile:
    psi: float
    ne: float
    te: float
    ti: float

    def nesep_neped(self) -> float:
        return self.ne[-1] / 3.48


class mtanh_fit_pars():
    def mtanh(self):
        psi = np.linspace(0, 1, 200)

        # I ALWAYS GET NANE FROM THE SECOND POWER AND i DONT KNOW WHY!!!!
        temp = (1 - (psi / self.psi_ped) ** self.alphaT1) ** self.alphaT2

        # THIS IS VEDRY WRONG!!!!! SHOYLD CHECK WHY YOU GET NANS
        temp_array = np.nan_to_num(temp)
        profile = self.sep + self.a0 * (np.tanh((2 * (1 - self.psi_mid) / self.width)) - np.tanh(
            2 * (psi - self.psi_mid) / self.width)) + self.an1 * np.heaviside((1 - psi / self.psi_ped), 0) * temp_array

        return psi, profile

    def mtanh_minus_inifinity(self):
        # remove the core part
        profile = self.sep + self.a0 * (np.tanh((2 * (1 - self.psi_mid) / self.width)) + 1)
        return profile

    def __init__(self, fit_pars):
        self.a0 = float(fit_pars[0])
        self.sep = float(fit_pars[1])
        self.an1 = float(fit_pars[2])
        self.psi_mid = float(fit_pars[3])
        self.width = float(fit_pars[4])
        self.alphaT1 = float(fit_pars[5])
        self.alphaT2 = float(fit_pars[6])

        self.height = self.a0 * 2
        self.psi_ped = 1 - self.width

        psi, profile = self.mtanh()
        profile_minus_infinity = self.mtanh_minus_inifinity()
        self.profile = profile
        self.psi = psi
        self.profile_at_minus_infinity = profile_minus_infinity


def read_text_ouput(dir, name):
    path = dir + '/marginal_profs/' + name
    data = np.loadtxt(path)
    return data


def split_up_fit_pars(line):
    temp1 = line.split('=')
    temp2 = temp1[1].replace('[', '')
    temp3 = temp2.replace(']', '')
    temp4 = temp3.replace(';', '')
    fit_pars = temp4.split()
    return fit_pars

def split_teped(string):
    temp1 = string.split(':')
    temp2 = temp1[1].strip()
    return float(temp2)

def read_europed_output(dir, name):
    path = dir + '/output/' + name
    file = open(path, 'r')
    lines = file.readlines()

    te_prof_counter = 0
    ne_prof_counter = 0

    teped_eped_counter = 0
    teped_tanh_counter = 0

    profiles = {}


    #  initilialise objects mtanh_fit_pars fits
    for line in lines:


        if line.find('tepars') > -1:
            fit_pars = split_up_fit_pars(line)
            profiles['temp_crit_' + str(te_prof_counter)] = mtanh_fit_pars(fit_pars)
            print(fit_pars)

            te_prof_counter += 1

        if line.find('nepars') > -1:
            fit_pars = split_up_fit_pars(line)
            profiles['ne_crit_' + str(ne_prof_counter)] = mtanh_fit_pars(fit_pars)
            print(fit_pars)

            ne_prof_counter += 1

    # Now fill that object with stuff you need, by looping thorough the file again
    #  this is HACK! and slow
    for line in lines:
        if line.find('Critical Teped (EPED)') > -1:
            eped_teped = split_teped(line)
            profiles['temp_crit_' + str(teped_eped_counter)].eped_teped = eped_teped
            teped_eped_counter += 1

        if line.find('Critical Teped (tanh)') > -1:
            mtanh_teped = split_teped(line)
            profiles['temp_crit_' + str(teped_tanh_counter)].mtanh_teped = mtanh_teped
            teped_tanh_counter += 1


    return profiles


def read_data(path, name):
    data = read_text_ouput(path, name + '.crit1')
    critical_profile_1 = CriticalProfile(data[:, 0], data[:, 1], data[:, 2], data[:, 3])
    data = read_text_ouput(path, name + '.crit2')
    critical_profile_2 = CriticalProfile(data[:, 0], data[:, 1], data[:, 2], data[:, 3])
    profiles = read_europed_output(path, name)

    return critical_profile_1, critical_profile_2, profiles


def plot_profiles(crit_profiles, profiles, names, colours, axes):
    # for label, crit_profile in crit_profiles.items():

    for label, crit_profile_keys, profile_key, colour in zip(names, crit_profiles, profiles, colours):


        axes[0].plot(crit_profiles[crit_profile_keys].psi, crit_profiles[crit_profile_keys].ne*1e19,
                     label=label, color=colour, linestyle='--')
        axes[0].axvline(((profiles[profile_key]['ne_crit_0'].psi_ped)),color=colour, linestyle='--')


        axes[1].plot(crit_profiles[crit_profile_keys].psi, crit_profiles[crit_profile_keys].te*1e3,
                     label=label, color=colour, linestyle='--')
        axes[1].axvline(((profiles[profile_key]['temp_crit_0'].psi_ped)),color=colour, linestyle='--')
def plot_ped_top(crit_profiles, profiles, names, colours, ped_top_axes, markers):
    te_ped_top_ax,ne_ped_top_ax, pe_ped_top_ax = ped_top_axes
    nesep_l = []
    peped_l = []

    for label, crit_profile_keys, profile_key, colour, marker in zip(names, crit_profiles, profiles, colours, markers):

        nesep = (crit_profiles[crit_profile_keys].ne[-1])

        neped = 3.48
        print(profile_key)
        print(profiles[profile_key])



        te_ped_top_ax.plot(nesep,(profiles[profile_key]['temp_crit_0'].eped_teped),
                     label=label, color=colour, marker=marker, ms=10, alpha=0.5)

        ne_ped_top_ax.plot(nesep,neped,
                     label=label, color=colour, marker=marker, ms=10, alpha=0.5)

        peped = ((profiles[profile_key]['temp_crit_0'].eped_teped)*1e3 * neped*1e19 * 1.602e-19)/1e3
        peped_l.append(peped)
        nesep_l.append(nesep)
        # pe_ped_top_ax.plot(nesep,peped,
        #              label=label, color=colour, marker='*', ms=10, alpha=0.5)

    pe_ped_top_ax.plot(np.array(nesep_l),np.array(peped_l), '-*', ms=10, alpha=0.5)

    pe_ped_top_ax.legend(fontsize=9)

def read_plot_europed_data(axes, ped_top_axes):
    crit_profiles_1 = {}
    crit_profiles_2 = {}
    profiles = {}

    # names = ['jet96202_m18-20_shift01_mishka']
    # paths = ['/home/ssaar/LINUX/europed/']
    #
    # names = ['jet96202_m18-20_shiftm005_mishka', 'jet96202_m18-20_shift01_mishka', 'jet96202_m18-20_shift02_mishka',
    #          'jet96202_m18-20_shift005_mishka', 'jet96202_m18-20_shiftm01_mishka', 'jet96202_m18-20_shiftm02_mishka']
    # paths = ['/home/ssaar/LINUX/europed/'] * 6

    #
    # names = ['jet96202_m18-20_shiftm005_mishka', 'jet96202_m18-20_shift005_mishka','jet96202_m18-20_shift01_mishka',
    #          'jet96202_m18-20_shift02_mishka']
    # paths = ['/home/ssaar/LINUX/europed/'] * 4
    # names = ['jet96202_m18-20_shiftm005_mishka', 'jet96202_m18-20_shiftm005_mishka_nosmart',
    #          'jet96202_m18-20_shift01_mishka', 'jet96202_m18-20_shift01_sauter_mishka_nosmart']
    # paths = ['/home/ssaar/LINUX/europed/']*4

    names = ['jet96202_m18-20_shiftm005', 'jet96202_m18-20_shift01', 'jet96202_m18-20_shift02']
    paths = ['/home/lfrassin/work/europed/europed/']*3

    # names =  ['jet96202_m18-20_shiftm005_sauter_mishka_nosmart', 'jet96202_m18-20_shift01_sauter_mishka_nosmart',
    #          'jet96202_m18-20_shift02_sauter_mishka_nosmart']
    #
    #
    # paths =  ['/home/ssaar/LINUX/europed/'] * 3

    # names = ['jet96202_m18-20_shift02_mishka_nosmart','jet96202_m18-20_shift01_mishka_nosmart',
    #          'jet96202_m18-20_shift005_mishka_nosmart', 'jet96202_m18-20_shiftm005_mishka_nosmart',
    #          'jet96202_m18-20_shiftm01_mishka_nosmart', 'jet96202_m18-20_shiftm02_mishka_nosmart']
    #
    # paths = ['/home/ssaar/LINUX/europed/'] * 6

    # names = names + ['jet96202_m18-20_shift02_sauter_mishka_nosmart','jet96202_m18-20_shift01_sauter_mishka_nosmart',
    #          'jet96202_m18-20_shiftm005_sauter_mishka_nosmart','jet96202_m18-20_shiftm005_sauter_mishka_nosmart',
    #          'jet96202_m18-20_shift01_sauter_mishka_nosmart','jet96202_m18-20_shift02_sauter_mishka_nosmart']
    #
    #
    # paths = paths + ['/home/ssaar/LINUX/europed/'] * 6


    colours = ['k', 'k','k', 'k','k','k', 'r','r','r','g','g','g','g','g','g']
    markers = ['*','*','*','*','*','*','d','d','d','^','^','^','^','^','^']
    labels = ['0.2 L']*len(markers)

    for path, name in zip(paths, names):
        critical_profile_1A, critical_profile_2A, profiles_A = read_data(path, name)
        crit_profiles_1[name] = critical_profile_1A
        crit_profiles_2[name] = critical_profile_2A

        profiles[name] = profiles_A
        labels.append(critical_profile_1A.nesep_neped())

    plot_profiles(crit_profiles_1, profiles, labels, colours, axes)
    plot_ped_top(crit_profiles_1, profiles, labels, colours, ped_top_axes, markers)

    plt.show()
