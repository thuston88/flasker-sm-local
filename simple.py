
# return list of institutions and id's 

def get_all_spots():
    unique_second_elements = set()
    result_tuples = []

    spots = Assets.query
    ####
    table = Table(title="Institutions")
    table.add_column("Id", justify="right", style="cyan", no_wrap=True)
    table.add_column("Institution", justify="right", style="cyan", no_wrap=True)

    """
    set_table = Table(title="Unique Institutions")
    set_table.add_column("Id", justify="right", style="cyan", no_wrap=True)
    set_table.add_column("Institution", justify="right", style="cyan", no_wrap=True)
    """

    spots_list = []

    for p in spots:
        sid = str(p.id)
        table.add_row(sid, p.institution)

        spots_tup = (sid, p.institution)
        spots_list.append(spots_tup)

    console = Console()
    console.print(table)

    # print(f'{spots_list=}')
    # print(f'spots is: {spots}')

    for ctr, tuple_element in enumerate(spots_list):
        # print(f'{tuple_element=}')
        _, second_element = tuple_element  # Unpacking the tuple to get the second element
        if second_element not in unique_second_elements:
            unique_second_elements.add(second_element)
            tup = (ctr,tuple_element[1])
            # print(f'{tup=}')
            # result_tuples.append(tuple_element)
            result_tuples.append(tup)

    print(f'{result_tuples=}')
    return result_tuples
    ####
    # return spots

####################################
####################################

@app.route('/simple', methods=['GET', 'POST'])
def simple():

    form = SimpleForm()

    form.institution.choices = get_all_spots()
    # form.institution.choices = [(sid, sinstit) for spot in get_all_spots()]

    if form.validate_on_submit():
        print(f'institution on form: {form.institution.data}')
        """
        # user = Users.query.filter_by(username=form.username.data).first()

        # for row in user:
        #    print(f' username: {row.username} -  password: {row.password_hash}')

        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfull!!")
                return redirect(url_for('option'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")

    else:
        print("form did not validate")
        print(f'user name on form: {form.username.data}')

        user = Users.query

        for row in user:
            print(f' username: {row.username} -  password: {row.password_hash}')


        # flash("Form is not validated")
        """
    return render_template("simple.html", form=form, choices=form.institution.choices)

