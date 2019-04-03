import os
import glob
import subprocess
from PIL import Image
from PIL import ImageChops

import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_files_in_dir(path):
    """
    Get all file names in specified path. (require python 3.5*).
    :param path:
    :return:
    """
    files = [os.path.basename(f) for f in glob.glob(path + "*.pdf")]
    return files


def get_files_in_dir2(path):
    """
    Depreciated
     Get all file names in specified path. (before python 3.5*).
    :param path:
    :return:
    """
    files = []
    for root, directories, file_list in os.walk(path):
        for filename in file_list:
            # if '.pdf' in filename:
            if filename.endswith('.pdf'):
                files.append(filename)
    return files


def compare_filenames(file_list1, file_list2):
    """
    Compare elements in 2 lists.
    :param file_list1:
    :param file_list2:
    :return:
    """
    return set(file_list1).difference(file_list2)


def common_filenames(file_list1, file_list2):
    """
    Find elements common in 2 lists
    :param file_list1: a list to compare
    :param file_list2: a list to compare
    :return: list of common items
    """
    return set(file_list1).intersection(file_list2)


def call_convert(path, src_filename, dest_filename):
    """
    Call convert to convert pdf to png using ImageMagick and GhostScript.
    WARNING: ImageMagick and GhostScript needs to be setup and executable from command prompt.
    :param path: directory to execute 'convert' command
    :param src_filename: source filename to pass to the 'convert' statement
    :param dest_filename: output filename of 'convert' statement
    """
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.check_call(["convert", src_filename, dest_filename], shell=False, cwd=path, stdout=FNULL,
                              stderr=subprocess.STDOUT)

        # '-append' option concatenates all images to a single file. However, there's a bug.
        # subprocess.check_call(["convert", src_filename, "-append", dest_filename], shell=False, cwd=path)
    except Exception as e:
        logger.error('Error converting pdf to an image.', exc_info=True)
        logger.error(e)
    else:
        logger.info('convert file ' + src_filename + ' to ' + dest_filename)


def compare_pdf_file(path1, path2):
    """
    Compare content of 2 pdf files by converting pages to png image files
    :param path1: path of the pdf file to compare
    :param path2:  path of the pdf file to compare
    :return: difference of image files
    """
    img1 = Image.open(path1)
    img2 = Image.open(path2)

    imDiff = ImageChops.difference(img1, img2).getbbox()
    return imDiff

    # WARNING: can't not just do binary comparison of pdf files because of creation date timestamp in pdf files
    # return filecmp.cmp(imagePath1, imagePath2, shallow=False)


def convert_pdf2png(path, img):
    """
    Convert pdf file to png image fil (per pdf page)
    :param path: path to pdf file to convert
    :param img: directory to output image files
    """
    if not os.path.isdir(path+'/'+img):
        os.mkdir(path+'/'+img)

    files_list = get_files_in_dir(path)

    for file in files_list:
        call_convert(path, file, img + '/' + file[:-3] + 'png')


def compare_reports(org_dir='./output_original/', cur_dir='./output/', img='img'):
    """
    Compare pdf files in specified directories.
    :param org_dir: directory containing pdf files to compare against
    :param cur_dir: directory containing pdf files to test
    :param img: subdirectory name to generate image files
    :return:
    """
    files_in_org_dir = get_files_in_dir(org_dir)
    files_in_test_dir = get_files_in_dir(cur_dir)

    # test if same number of files
    if len(files_in_org_dir) != len(files_in_test_dir):
        logger.error('number of files in test directory is different. should be: ' + str(len(files_in_org_dir))
                     + ' test directory: ' + str(len(files_in_test_dir)))
    else:
        logger.info('number of files in directories match: ' + str(len(files_in_org_dir)))

    # check for missing or additional generated files
    missing_files = compare_filenames(files_in_org_dir, files_in_test_dir)
    additional_files = compare_filenames(files_in_test_dir, files_in_org_dir)
    if len(missing_files) > 0:
        logger.error('missing:', missing_files)
    if len(additional_files) > 0:
        logger.error('Additional files:', additional_files)

    # compare content of pdf
    common_files = [f[:-4] for f in common_filenames(files_in_org_dir, files_in_test_dir)]

    # convert pdf in test directory to images
    convert_pdf2png(cur_dir, img)

    for file in common_files:
        image_list_org = [os.path.basename(f) for f in glob.glob(org_dir + img + '/' + file + "*.png")]
        image_list_test = [os.path.basename(f) for f in glob.glob(cur_dir + img + '/' + file + "*.png")]

        if len(image_list_org) != len(image_list_test):
            logger.error("number of pages is different in report '" + file + "'.pdf'. original pages:"
                         + str(len(image_list_org)) + "' test pages:" + str(len(image_list_test)))
        else:
            # check for missing or additional generated files
            missing_pages = compare_filenames(image_list_org, image_list_test)
            additional_pages = compare_filenames(image_list_test, image_list_org)
            if len(missing_pages) > 0:
                logging.error('missing pages:', missing_pages)
            if len(additional_files) > 0:
                logging.error('Additional pages:', additional_pages)

            # check content of pages
            if len(missing_pages) == 0 and len(additional_pages) ==0:
                for img_file in image_list_test:
                    result = compare_pdf_file(org_dir + img + '/' + img_file, cur_dir + img + '/' + img_file)
                    if not file.startswith('pdf_current_date') and result is not None:
                        logging.error('content of file ' + file + ' is different')


if __name__ == '__main__':
    org = './output_original/'
    cur = './output/'
    img_sub = 'img'

    # uncomment to convert original test directory pdf files
    # convert_pdf2png(org, img)

    compare_reports(org, cur, img_sub)




