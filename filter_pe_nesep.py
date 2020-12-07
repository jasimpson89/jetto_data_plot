import read_ped_db
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt


def filter_dataframe(df):
    pass


def plot_pe_nesep():
    df = read_ped_db.read_ped()
    df.columns

    # selected current
    max_current = 2.1
    min_current = 1.9

    # select toroidal field
    max_field = 2.1
    min_field = 1.9

    # selected traiangularity
    # low triangularity
    delta = 0.3

    # selected P NBI
    lower_nbi = 9
    max_lower = 11

    selected_peped_nesep = (df[
        (df.Ip > min_current) & (df.Ip < max_current) & (df.Bt > min_field) & (df.Bt < max_field) & (
                    df.triangularity < delta) & (df.pnbi > lower_nbi) & (df.pnbi < max_lower)])

    # found data
    # selected_peped_nesep=selected_pnbi
    plt.figure(1)

    plt.plot(selected_peped_nesep.nesep, selected_peped_nesep.peped, 'r*')

    plt.figure(2)
    plt.plot(selected_peped_nesep.nesep, selected_peped_nesep.neped, 'b*')

    plt.figure(3)
    plt.plot(selected_peped_nesep.nesep, selected_peped_nesep.teped, 'g*')


plot_pe_nesep()
plt.figure(1)
plt.savefig('./peped.png')
plt.figure(2)
plt.savefig('./neped.png')
plt.figure(3)
plt.savefig('./teped.png')

plt.show()
