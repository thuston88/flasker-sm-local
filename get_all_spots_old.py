
####################################
def get_all_spots_old():
    spots = Assets.query
    ####
    table = Table(title="Institutions")
    # table.add_column("Id", justify="right", style="cyan", no_wrap=True)
    table.add_column("Institution", justify="right", style="cyan", no_wrap=True)

    set_table = Table(title="Unique Institutions")
    # set_table.add_column("Id", justify="right", style="cyan", no_wrap=True)
    set_table.add_column("Institution", justify="right", style="cyan", no_wrap=True)

    spots_list = []
    spots_tup = ()

    for p in spots:
        # sid = str(p.id)
        table.add_row(p.institution)
    console = Console()
    console.print(table)

    print(f'spots is: {spots}')

    insts = [(i.institution) for i in spots]
    print(f'insts: {insts}')

    """
    set_spots = set(insts)
    # print(f'set_spots is: {set_spots}')

    for p in set_spots:
        sid = str(p.id)
        set_table.add_row(sid, p.institution)
    console = Console()
    console.print(set_table)
    """

    ####
    return spots

