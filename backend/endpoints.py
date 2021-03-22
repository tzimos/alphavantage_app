from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from backend.constants import (
    GLOBAL_QUOTE,
    SYMBOL_SEARCH,
)
from backend.external_service import perform_request
from backend.forms import ApiKeyForm
from backend.utils import camel_case_to_title_case

blueprint = Blueprint("api", __name__)


@blueprint.route("/", methods=["POST", "GET"])
def register_api_key():
    """Register api-key in the flask session for later usage."""
    form = ApiKeyForm()
    if request.method == "GET":
        return render_template("api_key.html", form=form)

    form = ApiKeyForm(request.form)
    if form.validate():
        form.save()
        return redirect(url_for("api.symbol_search"))
    else:
        return render_template("api_key.html", form=form)


@blueprint.route("/symbol_search", methods=["POST", "GET"])
def symbol_search():
    api_key = session.get("api_key")
    if not api_key:
        return redirect(url_for("api.register_api_key"))

    if request.method == "GET":
        return render_template("symbol_search.html")
    keywords = request.form["query"]

    return jsonify(
        perform_request(
            apikey=api_key,
            function=SYMBOL_SEARCH,
            keywords=keywords
        )
    )


@blueprint.route(
    "/symbol_search_analytical/<string:symbol>", methods=["GET"])
def symbol_search_analytical(symbol):
    api_key = session.get("api_key")
    if not api_key:
        return redirect(url_for("api.register_api_key"))

    processed_data = perform_request(
        apikey=api_key,
        function=SYMBOL_SEARCH,
        keywords=symbol,
        exact_match=symbol,
    )
    if not processed_data:
        error = {
            "message": f"Unable to find a matching symbol. "
                       f"Maybe you need to "
                       f"<a href='{url_for('api.symbol_search')}'>"
                       f"try searching again a symbol</a>"
        }
        return render_template("symbol_search_analytical.html", error=error)
    col_names = [list(elem.keys()) for elem in processed_data][0]
    columns = camel_case_to_title_case(col_names)

    return render_template(
        "symbol_search_analytical.html",
        data=processed_data,
        columns=columns
    )


@blueprint.route("/historical_data/<string:symbol>", methods=["GET", "POST", ])
def historical_data(symbol):
    api_key = session.get("api_key")
    if not api_key:
        return {"redirect": url_for("api.register_api_key")}, 403
    if request.method == "GET":
        return render_template("historical_data.html", symbol=symbol)
    params = {
        "function": request.form["function"],
        "symbol": symbol or request.form["symbol"],
        "interval": request.form.get("interval"),
    }
    processed_data = perform_request(
        apikey=api_key,
        **params,
    )
    if processed_data.get("error"):
        flash(processed_data.get("error"))
        return {"redirect": url_for("api.register_api_key")}, 400
    return jsonify(processed_data)


@blueprint.route("/current-quote/<string:symbol>", methods=["GET", "POST"])
def current_quote(symbol):
    api_key = session.get("api_key")
    if not api_key:
        return redirect(url_for("api.register_api_key"))
    processed_data = perform_request(
        apikey=api_key,
        function=GLOBAL_QUOTE,
        symbol=symbol,
    )
    if processed_data.get("error"):
        flash(processed_data.get("error"))
        return redirect(url_for("api.register_api_key"))
    columns = camel_case_to_title_case(list(processed_data.keys()))
    return render_template(
        "current_quote.html",
        columns=columns,
        data=processed_data,
        symbol=symbol,
    )
