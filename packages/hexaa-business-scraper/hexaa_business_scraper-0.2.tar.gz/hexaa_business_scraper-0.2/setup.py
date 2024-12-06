from setuptools import setup, find_packages

setup(
    name="hexaa_business_scraper",
    version="0.2",
    description="A Flask-based business scraper leveraging Playwright and Google Maps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dilawaiz Khan",  # Replace with your name
    author_email="dilawaizkhan08@gmail.com",  # Replace with your email
    url="https://github.com/your_username/hexaa_business_scraper",  # Update with your repository URL
    license="MIT",  # Or your chosen license
    packages=find_packages(),
    include_package_data=True,  # Ensures templates/static files are included
    install_requires=[
        "flask",
        "playwright",
        "pandas",
        "flask-cors",  # Updated naming for Flask-CORS
    ],
    entry_points={
        'console_scripts': [
            'hexaa_business_scraper=google_maps_scraper.main:scrape_data_cli',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
