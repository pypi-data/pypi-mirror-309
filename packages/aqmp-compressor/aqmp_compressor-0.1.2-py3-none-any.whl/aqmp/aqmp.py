import numpy as np
from .rawfile import RawFile
from .omp import OMPHandler
from .utility import Utility
from PIL import Image
import zlib  # to apply DEFLATE

# Codec nuevo nombre para la clase?


class ImageCompressor:
    """
    Class for compressing and decompressing images
    """

    def __init__(
        self,
        min_sparcity,
        min_n,
        max_n,
        a_cols,
        max_error,
        wavelet_election="db1",
        shuffle_dictionary=False,
        v_format_precision="f",
        apply_deflate=False,
    ):
        # Algorithm Parameters
        self.min_n = min_n
        self.max_n = max_n
        self.a_cols = a_cols
        self.min_sparcity = min_sparcity
        self.max_error = max_error
        self.v_format_precision = v_format_precision
        self.apply_deflate = apply_deflate

        # Other File Format parameters (No son más argumentos de la clase)
        self.fif_version = 2
        self.magic_number = b"FIF"  # Ensure this is a bytes object
        self.header_format = "3sBiiBBBBB"

        self.omp_handler = OMPHandler(
            self.min_n, self.max_n, self.a_cols, self.min_sparcity, self.max_error
        )
        self.omp_handler.initialize_dictionary(
            # wavelet_election = wavelet_election,
            # shuffle = shuffle_dictionary
        )

    def encode(self, input_file, output_file):
        """Compress input_file with the given parameters into output_file"""

        image = Image.open(input_file)
        image = image.convert("YCbCr")  # por que esta eleccion en lugar de RGB?
        w, h = image.size
        depth = Utility.mode_to_bpp(image.mode) // 8
        self.image_rawsize = w * h * depth  # no usado hasta ahora
        self.processed_blocks = 0
        self.non_zero_coefs = 0

        with RawFile(output_file, "wb") as file:

            file.write_header(
                self.header_format,
                self.magic_number,
                self.fif_version,
                w,
                h,
                depth,
                0,  # A_id (to be removed)
                0,  # basis_index (to be removed)
                self.min_n,
                self.max_n,
            )

            image_data = np.array(image.getdata()).reshape(h, w, depth)

            n = self.max_n
            x_list = []
            for k in range(depth):
                channel_processed_blocks, x_list = self.omp_handler.omp_encode(
                    x_list=x_list,
                    image_data=image_data[:, :, k],
                    max_error=self.max_error,
                    block_size=n,
                    k=k,
                )
                self.processed_blocks += channel_processed_blocks

            for n, i, j, k, x in x_list:
                file.write("H", i)
                file.write("H", j)
                file.write("B", k)
                file.write("B", n)

                x = Utility.quantize(x, self.v_format_precision).tolist()
                x_norm_0 = np.linalg.norm(x, 0)
                self.non_zero_coefs += x_norm_0

                file.write_vector(x, x_norm_0, self.v_format_precision)
                # print("i, j, k, n: ", i, j, k, n)

            file.write("I", self.processed_blocks)

            bytes_written = file.tell()
        print(f"processed_blocks: {self.processed_blocks}")
        print(f"bytes_written (without DEFLATE): {bytes_written}")

        if self.apply_deflate == True:
            ## apply DEFLATE compression
            with open(output_file, "rb") as file:
                compress = zlib.compressobj(
                    9, zlib.DEFLATED, 15, 9, zlib.Z_DEFAULT_STRATEGY
                )  # ver estos parametros
                zdata = compress.compress(file.read())
                zdata += compress.flush()

            with open(output_file, "wb") as file:
                file.write(zdata)
                print(f"DEFLATE applied. Bytes to write: {file.tell()}")

        print("File saved.")

    def decode(self, input_file, output_file):
        """Decompress input_file into output_file"""

        if self.apply_deflate == True:
            # se descomprime el archivo al que se le aplicó DEFLATE
            with open(input_file, "rb") as file:
                decompress = zlib.decompressobj(
                    15
                )  # 15 is the window size (must match the compress settings)
                decompressed_data = decompress.decompress(file.read())
                decompressed_data += decompress.flush()

            new_file = input_file + "_after_deflate"
            with open(new_file, "wb") as file:
                file.write(decompressed_data)
            input_file = new_file

        with RawFile(input_file, "rb") as file:
            file.seek(-4, 2)
            processed_blocks = file.read("I")
            file.seek(0)
            # print("processed_blocks:",processed_blocks)
            # No es necesario ya que la clase guarda estos parámetros
            # A_id, basis_index = 0, 0 (to be removed)
            magic_number_read, version, w, h, depth, A_id, basis_index, min_n, max_n = (
                file.read(self.header_format)
            )
            # print(magic_number_read, version, w, h, depth, A_id, basis_index, min_n, max_n)

            if magic_number_read != self.magic_number.decode("utf-8"):
                raise Exception(
                    f"Invalid image format: Wrong magic number '{magic_number_read}'"
                )

            if version != self.fif_version:
                raise Exception(
                    f"Invalid codec version: {version}. Expected: {self.fif_version}"
                )

            image_data = np.zeros((h, w, depth), dtype=np.float32)
            image_data = self.omp_handler.omp_decode(
                file, image_data, self.v_format_precision, processed_blocks
            )

            if depth == 1:
                image_data[:, :, 1] = image_data[:, :, 0]
                image_data[:, :, 2] = image_data[:, :, 0]

            image_data = Utility.ycbcr_to_rgb(image_data)
            image = Image.fromarray(image_data.astype("uint8"))
            image.save(output_file)
            print("Output file saved to: " + output_file)
