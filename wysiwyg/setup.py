from distutils.core import setup

setup(name='jupyter_wysiwyg',
      packages=['jupyter_wysiwyg'],
      version='0.1.0',
      description='WYSIWYG editing functionality for markdown/HTML cells in Jupyter',
      license='BSD',
      author='Thorin Tabor',
      author_email='thorin@broadinstitute.org',
      url='https://github.com/genepattern/genepattern-notebook/tree/master/wysiwyg',
      download_url='https://github.com/genepattern/genepattern-notebook/archive/0.5.0.tar.gz',
      keywords=['genepattern', 'wysiwyg', 'ipython', 'jupyter'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Framework :: IPython',
      ],
      install_requires=[
          'jupyter',
          'notebook>=4.2.0',
      ],
      package_data={'jupyter_wysiwyg': ['static/index.js', 'static/ckeditor/*']},
      )