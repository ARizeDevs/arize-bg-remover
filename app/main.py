from flask import Flask, request, send_file
from rembg import remove
from io import BytesIO
import requests

app = Flask(__name__)


@app.route("/removebg", methods=["POST"])
def remove_background():
    image_url = request.json.get("image_url")
    signed_url = request.json.get("signed_url")

    try:
        response = requests.get(image_url)
        response.raise_for_status()

        if "image" not in response.headers["Content-Type"]:
            return {"error": "URL does not point to an image"}, 400

        input_image = response.content
        output_image = remove(input_image)

        # If a signed URL is provided, upload the processed image to GCS
        if signed_url:
            upload_response = requests.put(
                signed_url, data=output_image, headers={"Content-Type": "image/png"}
            )
            upload_response.raise_for_status()
            return {"status": "done"}, 200

        # If no signed URL is provided, return the processed image
        else:
            print("No signed URL provided")
            return send_file(BytesIO(output_image), mimetype="image/png")

        return send_file(BytesIO(output_image), mimetype="image/png")

    except requests.RequestException as e:
        return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
