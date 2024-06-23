import cv2
from pyzbar.pyzbar import decode

cam = cv2.VideoCapture(0)

cv2.namedWindow("QR Scanner Barcode")

# Buka file teks untuk menulis data barcode
with open("QR code_data.txt", "w") as barcode_file:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("QR Scanner Barcode", frame)

        # Decode barcodes
        barcodes = decode(frame)
        
        for barcode in barcodes:
            # Extract barcode data and write it to the text file
            data = barcode.data.decode("utf-8")
            barcode_file.write(f"QR Scanner data:\n{data}\n")

            # Draw a rectangle around the barcode on the frame
            points = barcode.polygon
            if len(points) == 4:
                pts = [(point.x, point.y) for point in points]
                pts = [(int(x), int(y)) for x, y in pts]
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, data, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                print(f"Barcode data: {data}")

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

# Close the text file
barcode_file.close()

cam.release()
cv2.destroyAllWindows()