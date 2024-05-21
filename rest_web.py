#Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175


from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector

app = Flask(__name__, static_url_path='')

# Connect to database
conn = mysql.connector.connect(user='root', password='',
                               host='127.0.0.1',
                               database='zipcodes',
                               buffered=True)
cursor = conn.cursor()


# Update zip code database population for a specified zip code
@app.route('/searchZIP/<searchZIP>')
def searchZIP(searchZIP):
    # Execute SQL query to check if the provided zip code exists
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchZIP,])
    # Get the number of rows returned by the query
    result_count = cursor.rowcount
    # Check if the zip code exists in the database
    if result_count != 1:
        return f"The Zip Code {searchZIP} was not found."
    else:
        searched_data = cursor.fetchall()
        return f"Success! Here is the information for Zip Code: %s" % searched_data


# Update zip code database population for a specified zip code
@app.route('/updatezippop/<updateZIP> <updatePOP>')
def updatezippop(updateZIP, updatePOP):
    # Execute SQL query to check if the provided zip code exists
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", (updateZIP,))
    # Get the number of rows returned by the query
    result_count = cursor.rowcount
    # Check if the zip code exists in the database
    if result_count != 1:
        return f"The zip Code {updateZIP} was not found."
    else:
        cursor.execute("UPDATE `zipcodes` SET Population = %s WHERE zip= %s;", (updatePOP, updateZIP))
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s and Population=%s", (updateZIP, updatePOP))
        # Check if the population has been updated successfully
        verification_count = cursor.rowcount
        if verification_count != 1:
            f"Failed to update population for Zip Code: {updateZIP}"
        else:
            return f"Population has been updated successfully for Zip Code: {updateZIP}"


# update webpage
@app.route('/update', methods=['POST'])
def update():
    # Retrieve the zip code and population from the form data
    user_zip = request.form['uzip']
    user_pop = request.form['upop']
    return redirect(url_for('updatezippop', updateZIP=user_zip, updatePOP=user_zip))


# search page
@app.route('/search', methods=['GET'])
def search():
    user_zip = request.args.get('szip')
    return redirect(url_for('searchZIP', searchZIP=user_zip))


# Root of web server and goes to template (login.html)
@app.route('/')
def root():
    return render_template('login.html')


# Main
if __name__ == '__main__':
    app.run(debug=True)
