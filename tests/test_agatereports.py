import os
import glob

from tests.generate_test_pdf import generate_test_pdf
from tests.compare_results import get_files_in_dir, compare_filenames, common_filenames, compare_pdf_file,\
    convert_pdf2png

from demos import *


class TestAgateReports(object):
    test_dir = 'output'             # directory containing report files to be tested
    base_dir = './output_original/'  # directory containing base report files
    img_dir = 'img'

    demo_dir = '../demos/'          # demo py file directory
    demo_base_dir = './output_demo/'  # to generate base demo pdf

    @staticmethod
    def compare_number_of_generated_files(base_dir_files, test_dir_files):
        """
        Test if the number of generated files matches with the expected number of files.
        """
        assert len(base_dir_files) == len(test_dir_files)

    @staticmethod
    def check_missing_files(base_dir_files, test_dir_files):
        """
        Test if there was ungenerated file.
        """
        missing_files = compare_filenames(base_dir_files, test_dir_files)
        assert len(missing_files) == 0

    @staticmethod
    def check_additional_files(base_dir_files, test_dir_files):
        additional_files = compare_filenames(base_dir_files, test_dir_files)
        assert len(additional_files) == 0

    @staticmethod
    def compare_pdf_content(base_dir_files, test_dir_files, test_dir,  base_dir, img_dir):
        # compare content of pdf
        common_files = [f[:-4] for f in common_filenames(base_dir_files, test_dir_files)]

        # convert pdf in test directory to images
        convert_pdf2png('./' + test_dir + '/', img_dir)

        for file in common_files:
            image_list_org = [os.path.basename(f) for f in glob.glob(base_dir + file + "*.png")]
            image_list_test = [os.path.basename(f) for f in glob.glob('./' + test_dir + '/' + file + "*.png")]

            assert len(image_list_org) == len(image_list_test)

            if len(image_list_org) == len(image_list_test):
                # check for missing or additional generated files
                missing_pages = compare_filenames(image_list_org, image_list_test)
                additional_pages = compare_filenames(image_list_test, image_list_org)

                assert len(missing_pages) == 0
                assert len(additional_pages) == 0

                # check content of pages
                if len(missing_pages) == 0 and len(additional_pages) ==0:
                    for img in image_list_test:
                        result = compare_pdf_file(base_dir + img, './' + test_dir + '/'+img)
                        if file.startswith('pdf_current_date'):  # current date report should be different
                            assert result is not None
                        else:
                            assert result is None

    @staticmethod
    def generate_demo_pdf(demo_dir, output_dir):
        # demo_dir = '../demos/'
        # demo_output_dir = './output_demo/'  # to generate base demo pdf
        demo_scripts = [os.path.basename(f)[:-3] for f in glob.glob(demo_dir + "*.py")]
        skip_list = ['__init__', 'run_all_samples']

        for demo in demo_scripts:
            if demo not in skip_list:
                script = demo + "." + demo + "_sample('../demos/jrxml/" + demo + ".jrxml', '" + output_dir + demo\
                         + ".pdf')"
                # script = demo + "." + demo + "_sample('../demos/jrxml/" + demo + ".jrxml', '../demos/output/"\
                #          + demo + ".pdf')"
                exec(script)

    def test_agatereports(self):
        """
        Execute scripts under 'tests' directory
        :return:
        """
        generate_test_pdf(self.test_dir)     # generate pdf files

        files_in_base_dir = get_files_in_dir(self.base_dir)
        files_in_test_dir = get_files_in_dir('./' + self.test_dir + '/')

        # check if the same number of pdf files were generated
        self.compare_number_of_generated_files(files_in_base_dir, files_in_test_dir)

        # check if some pdf files are missing
        self.check_missing_files(files_in_base_dir, files_in_test_dir)

        # check if there are additional files
        self.check_additional_files(files_in_test_dir, files_in_base_dir)

        # check if content of pdf files are the same
        self.compare_pdf_content(files_in_base_dir, files_in_test_dir, self.test_dir, self.base_dir,
                                 self.img_dir)

    def test_demo(self):
        """
        Execute scripts under 'demos' directory'
        """
        test_demo_dir = self.demo_dir + self.test_dir + "/"

        # self.generate_demo_pdf(self.demo_dir, self.demo_output_dir)    # uncomment to generate base demo pdf
        # convert_pdf2png(self.demo_base_dir, self.img_dir)              # uncomment to generate base demo/img files

        # self.generate_demo_pdf(self.demo_dir, test_demo_dir)    # generate pdf files

        files_in_base_dir = get_files_in_dir(self.demo_base_dir)
        files_in_test_dir = get_files_in_dir(test_demo_dir)

        # check if the same number of pdf files were generated
        self.compare_number_of_generated_files(files_in_base_dir, files_in_test_dir)

        # check if some pdf files are missing
        self.check_missing_files(files_in_base_dir, files_in_test_dir)

        # check if there are additional files
        self.check_additional_files(files_in_test_dir, files_in_base_dir)

        # check if content of pdf files are the same
        self.compare_pdf_content(files_in_base_dir, files_in_test_dir, test_demo_dir, self.demo_base_dir,
                                 self.img_dir)



