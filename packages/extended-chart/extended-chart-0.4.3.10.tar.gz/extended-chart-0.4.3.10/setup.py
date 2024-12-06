from setuptools import setup

setup(name='extended-chart',
      version='0.4.3.10',
      description='wrapper for lightweight-charts-python for trading strategy discovery',
      url='https://github.com/karunkrishna/extended_chart',
      author='Karun Krishna',
      author_email='karun.krishna@gmail.com',
      license='MIT',
      packages=['extended_chart', 'extended_chart.utils'],
      install_requires=['pywebview==4.4.1','lightweight-charts==1.0.18.9'],
      zip_safe=False
      )
