from PIL import Image
import io



async def create_collage(bot, photo1, photo2):


    file1 = await bot.get_file(photo1)
    file2 = await bot.get_file(photo2)



    img1_bytes = await file1.download_as_bytearray()
    img2_bytes = await file2.download_as_bytearray()



    img1 = Image.open(
        io.BytesIO(img1_bytes)
    ).convert("RGB")


    img2 = Image.open(
        io.BytesIO(img2_bytes)
    ).convert("RGB")



    height = min(
        img1.height,
        img2.height
    )



    img1.thumbnail(
        (
            height,
            height
        )
    )


    img2.thumbnail(
        (
            height,
            height
        )
    )



    collage = Image.new(
        "RGB",
        (
            img1.width + img2.width,
            height
        ),
        "white"
    )


    collage.paste(
        img1,
        (0,0)
    )


    collage.paste(
        img2,
        (
            img1.width,
            0
        )
    )



    output = io.BytesIO()


    collage.save(
        output,
        "JPEG"
    )


    output.seek(0)


    return output
