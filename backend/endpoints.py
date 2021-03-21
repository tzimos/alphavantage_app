from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from backend.constants import SYMBOL_SEARCH
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

    processed_data = perform_request(
        apikey=api_key,
        function=SYMBOL_SEARCH,
        keywords=keywords
    )
    return jsonify(processed_data)


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
