import json

from flask import abort, request, render_template, escape
from flask_user import current_user, login_required

from opencve.controllers.cves import CveController
from opencve.controllers.main import main
from opencve.utils import convert_cpes, get_cwes_details
from opencve.models.tags import Tag
from opencve.models.cve import Cve
from opencve.extensions import db


@main.route("/cve")
def cves():
    objects, metas, pagination = CveController.list(request.args)
    return render_template(
        "cves.html",
        cves=objects,
        vendor=metas.get("vendor"),
        product=metas.get("product"),
        pagination=pagination,
    )


@main.route("/cve/<cve_id>", methods=["GET"])
@login_required
def cve(cve_id):
    cve = CveController.get({"cve_id": cve_id})

    vendors = convert_cpes(cve.json["configurations"])
    cwes = get_cwes_details(
        cve.json["cve"]["problemtype"]["problemtype_data"][0]["description"]
    )

    # Add a tag
    if request.args.get("tag-plus"):

        tag_name = escape(request.args.get("tag-plus"))
        exists = Tag.query.filter(Tag.name == tag_name).filter(Tag.user_id == current_user.id).all()

        # Checks if tag already exists, else we create it
        if len(exists):
            tag = exists[0]
        else:
            tag = Tag(name=tag_name, user_id=current_user.id)
            db.session.add(tag)
            db.session.commit()

        # If the cve doesn't have this tag, we add it
        cve_req = Cve.query.filter(Cve.cve_id == escape(request.args.get("cve"))).all()[0]
        if tag not in cve_req.tags_id:
            cve_req.tags_id.append(tag)
            db.session.commit()

    # Delete a tag
    elif request.args.get("tag-moins"):

        cve_req = Cve.query.filter(Cve.cve_id == escape(request.args.get("cve"))).all()[0]
        tag = Tag.query.filter(Tag.name == escape(request.args.get("tag-moins"))).filter(Tag.user_id == current_user.id).all()[0]
        # Check if the cve has the tag
        if tag in cve_req.tags_id:
            cve_req.tags_id.remove(tag)
            db.session.commit()
        # Delete a tag if no cve uses it
        if not len(tag.cves.all()) - 1:
            db.session.delete(tag)
            db.session.commit()

    return render_template(
        "cve.html", cve=cve, cve_dumped=json.dumps(cve.json), vendors=vendors, cwes=cwes
    )
