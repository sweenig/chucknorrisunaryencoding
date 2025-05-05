import qrcode
import qrcode.constants

def generate_qr_code(data, filename="qr_code.png", error_correction:int=0, box_size:int=10, border:int=4, back_color:str="white", fill_color:str="black"):
    """
    Generate a QR code from input string and save it as an image
    
    Args:
        data (str): The string to encode in the QR code
        filename (str): The output filename (default: qr_code.png)
        error_correction (int): Error correction level (default: ERROR_CORRECT_L)
            - qrcode.constants.ERROR_CORRECT_L (0): About 7% error correction
            - qrcode.constants.ERROR_CORRECT_M (1): About 15% error correction
            - qrcode.constants.ERROR_CORRECT_Q (2): About 25% error correction
            - qrcode.constants.ERROR_CORRECT_H (3): About 30% error correction
        box_size (int): Size of each box in the QR code grid (default: 10)
        border (int): Thickness of the border (default: 4)
        back_color (str): Background color of the QR code (default: white)
        fill_color (str): Color of the QR code (default: black)
            Any colors from CSS (darkblue, lightgreen, etc.), from hex (#2f4f4f,
            #f5f5dc), or RGB ((34, 139, 34), (255, 255, 255)) can be used for
            both back_color and fill_color.
    """
    error_levels = [
        qrcode.constants.ERROR_CORRECT_L,
        qrcode.constants.ERROR_CORRECT_M,
        qrcode.constants.ERROR_CORRECT_Q,
        qrcode.constants.ERROR_CORRECT_H,
    ]
    qr = qrcode.QRCode( # Create QR code instance
        version=1,
        error_correction=error_levels[error_correction],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data) # add data
    qr.make(fit=True) # make the qr code
    qr_image = qr.make_image(fill_color=fill_color, back_color=back_color) # create the image
    qr_image.save(filename) # save the image
    return f"QR code saved as {filename}"

if __name__ == "__main__":
    import argparse
    # parse arguments
    args = argparse.ArgumentParser(description="Generate a QR code from a string")
    args.add_argument("data", type=str, help="The string to encode in the QR code")
    args.add_argument("-f", "--filename", type=str, default="qr_code.png", help="Output filename (default: qr_code.png)")
    args.add_argument("-e", "--error_correction", type=int, default=0, help="Error correction level 0 (Low), 1 (Medium), 2 (Quartile), 3 (High) (default: 0)")
    args.add_argument("-b", "--box_size", type=int, default=10, help="Size of each box in the QR code grid (default: 10)")
    args.add_argument("-B", "--border", type=int, default=4, help="Thickness of the border (default: 4)")
    args.add_argument("-c", "--back_color", type=str, default="white", help="Background color of the QR code (default: white)")
    args.add_argument("-C", "--fill_color", type=str, default="black", help="Color of the QR code (default: black)")
    args = args.parse_args()
    
    args_dict = vars(args)
    if not args.data:
        input_string = input("Enter the text for QR code: ")
        args_dict["data"] = input_string
    result = generate_qr_code(**args_dict) # generate the qr code
    print(result) # print the filename
    