import winzy
import glob
import imageio


def create_gif(pattern, output_file, fps, loop):
    if not output_file.lower().endswith((".gif")):
        print("Output file name should be .gif")
        output_file = f"{output_file}.gif"

    # Use glob to get all matching PNG files and sort them
    png_files = sorted(glob.glob(pattern))

    images = []
    for file_path in png_files:
        if file_path.endswith((".jpg", ".png", ".jpeg")):
            images.append(imageio.imread(file_path))

    # Add a pause at the end so that the viewers can ponder
    pause_images = [images[-1]] * (fps * 1)  # Pause for one second with given FPS
    images.extend(pause_images)

    # Save the images as a GIF with specified FPS
    imageio.mimsave(output_file, images, fps=fps, loop=loop)
    print(f"GIF saved to {output_file}")

def create_parser(subparser):
    parser = subparser.add_parser(
        "gif", description="Create gifs from bunch of files."
    )
    # Add subprser arguments here.
    parser.add_argument(
        "pattern",
        type=str,
        help="Pattern matching the PNG images (e.g., e:\\temp\\*.png)",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="animation.gif",
        help="Output GIF file name",
    )
    parser.add_argument(
        "-f", "--fps", type=int, default=10, help="Frames per second for the GIF"
    )

    parser.add_argument(
        "-l", "--loop", type=int, default=0, help="Loop for the GIF. 0 default"
    )

    return parser


class WinzyPlugin:
    """ Create gifs from files in a folder. """
    __name__ = "gif"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.main)

    def main(self, args):
        create_gif(args.pattern, args.output_file, args.fps, args.loop)

    def hello(self, args):
        # this routine will be called when "winzy gif is called."
        print("Hello! This is an example ``winzy`` plugin.")

gif_plugin = WinzyPlugin()
