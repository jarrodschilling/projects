# -------------- ADD PORTFOLIO 1 PAGE [GET] --------------------------------------------------------------------

@app.route("/add-portfolio1", methods=["GET"])
@login_required
def add_portfolio1_page():

    name = session.get("user_id")
    portfolio_id = "portfolio1"
    portfolio = get_port_name(name, portfolio_id)

    return render_template("add-portfolio1.html", portfolio_id=portfolio_id, portfolio=portfolio)


# -------------- ADD TO PORTFOLIO 1 [POST] --------------------------------------------------------------------

@app.route("/add-portfolio1", methods=["POST"])
@login_required
def add_portfolio1():

    # Pull data from user form
    name = session.get("user_id")
    portfolio_id = request.form.get("portfolio_id")
    symbols_list = request.form.getlist("symbols[]")
    error_symbol_list = []
    portfolio = get_port_name(name, portfolio_id)

    # Check that symbols are correct using yfinance and if they are add to database
    add_symbols(symbols_list, name, portfolio, portfolio_id, error_symbol_list)
    
    # For any symbols that are incorrect, let the user know what they are
    if len(error_symbol_list) != 0:
        return create_errors(f"Incorrect symbols: {error_symbol_list}. All other symbols added to portfolio {portfolio}")

    return redirect("/portfolio")