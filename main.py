import cv2
from pyzbar.pyzbar import decode
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Load the face cascade for face detection
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Streamlit setup
st.title("Barcode Scanner with Streamlit")
st.write("Tekan tombol 'Mulai' untuk membuka kamera dan mendeteksi barcode.")

# List to store detected barcodes
detected_barcodes = set()

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.i = 0  # Counter for face detection

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")  # Convert frame to OpenCV format
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        self.i += 1  # Increment the counter

        # Detect and annotate barcodes
        barcodes = decode(img)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            if barcode_data not in detected_barcodes:
                detected_barcodes.add(barcode_data)

                # Draw a rectangle around the barcode
                x, y, w, h = barcode.rect
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display barcode data and type on the frame
                text = f"{barcode_data} ({barcode_type})"
                cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Display barcode found message on Streamlit
                st.success(f"Barcode ditemukan: {barcode_data} ({barcode_type})")

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (95, 207, 30), 3)
            cv2.rectangle(img, (x, y - 40), (x + w, y), (95, 207, 30), -1)
            cv2.putText(img, 'F-' + str(self.i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        return img

# Streamlit button to start the video stream
if st.button("Mulai"):
    webrtc_streamer(
        key="example",
        video_transformer_factory=VideoTransformer,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )

# Display detected barcodes after stopping the video stream
if detected_barcodes:
    st.write("\nData barcode yang ditemukan:")
    for data in detected_barcodes:
        st.write(data)
