@app.route("/delete-portfolio1", methods=["POST"])
@login_required
def delete_portfolio1():

    name = session.get("user_id")
    portfolio_id = "portfolio1"
    symbols = request.form.getlist("symbols[]")

    # Delete symbols in symbol list from database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for i in range(0, len(symbols)):
        cursor.execute("DELETE FROM portfolios WHERE users_id = ? AND portfolio_id = ? AND symbol = ?", (name, portfolio_id, symbols[i],))

    conn.commit()
    conn.close()

    return redirect("/portfolio")


@app.route("/delete-portfolio1", methods=["GET"])
@login_required
def delete_portfolio1_page():

    name = session.get("user_id")
    portfolio_id = "portfolio1"
    portfolio = get_port_name(name, portfolio_id)

    # Render current portfolios
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM portfolios WHERE users_id = ?", (name,))
    investments = cursor.fetchall()
    
    cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio1' AND users_id = ?", (name,))
    portfolio1 = cursor.fetchall()
    
    
    portfolio1_name = portfolio_names(portfolio1)

    conn.commit()
    conn.close()

    return render_template("delete-portfolio1.html", portfolio_id=portfolio_id, portfolio=portfolio, investments=investments, portfolio1=portfolio1, portfolio1_name=portfolio1_name)
