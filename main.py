import cv2
from pyzbar.pyzbar import decode
import streamlit as st

# Streamlit setup
st.title("Barcode Scanner with Streamlit")
st.write("Tekan tombol 'Mulai' untuk membuka kamera dan mendeteksi barcode.")

# List untuk menyimpan data barcode yang sudah terdeteksi
detected_barcodes = set()

# Tombol untuk memulai scanner
if st.button("Mulai"):
    # Buka kamera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Error: Kamera tidak dapat dibuka.")
    else:
        st.write("Tekan 'q' di jendela kamera untuk keluar.")

        while True:
            # Baca frame dari kamera
            ret, frame = cap.read()
            if not ret:
                st.error("Tidak dapat membaca frame dari kamera.")
                break

            # Decode barcode pada frame
            barcodes = decode(frame)
            for barcode in barcodes:
                # Ambil data dari barcode
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type

                # Jika barcode belum terdeteksi sebelumnya, tambahkan ke log
                if barcode_data not in detected_barcodes:
                    detected_barcodes.add(barcode_data)

                    # Gambar kotak di sekitar barcode
                    x, y, w, h = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Tampilkan data dan jenis barcode di frame
                    text = f"{barcode_data} ({barcode_type})"
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Tampilkan data barcode di Streamlit
                    st.success(f"Barcode ditemukan: {barcode_data} ({barcode_type})")

            # Tampilkan frame di OpenCV window
            cv2.imshow("Barcode Scanner", frame)

            # Keluar jika tombol 'q' ditekan
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cetak semua data barcode yang terdeteksi setelah keluar
        st.write("\nData barcode yang ditemukan:")
        for data in detected_barcodes:
            st.write(data)

        # Lepaskan kamera dan tutup jendela
        cap.release()
        cv2.destroyAllWindows()