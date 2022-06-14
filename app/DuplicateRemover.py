from PIL import Image
import imagehash
import os


class DuplicateRemover:
    def __init__(self, dirname, logger, hash_size=8):
        self.dirname = dirname
        self.hash_size = hash_size
        self.logger = logger

    def find_duplicates(self):
        """
        Find and Delete Duplicates
        """
        fnames = os.listdir(self.dirname)
        hashes = {}
        duplicates = []
        for image in fnames:
            with Image.open(os.path.join(self.dirname, image)) as img:
                temp_hash = imagehash.average_hash(img, self.hash_size)
                if temp_hash in hashes:
                    duplicates.append(image)
                else:
                    hashes[temp_hash] = image

        if len(duplicates) != 0:
            space_saved = 0

            for duplicate in duplicates:
                space_saved += os.path.getsize(os.path.join(self.dirname, duplicate))

                os.remove(os.path.join(self.dirname, duplicate))
                self.logger.info("{} Duplicate Images successfully Deleted".format(duplicate))
