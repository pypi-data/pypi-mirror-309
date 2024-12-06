=========
poisson-d
=========


.. image:: https://img.shields.io/pypi/v/poisson-d.svg
        :target: https://pypi.python.org/pypi/poisson-d

.. image:: https://readthedocs.org/projects/poisson-d/badge/?version=latest
        :target: https://poisson-d.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Poisson disk implementation in python


* Free software: MIT license
* Documentation: https://poisson-d.readthedocs.io.


Features
--------

* Generate poisson disk coordinates on a grid
* Generate points with charactoristics of poisson disk from an image
* Generate points with charactoristics of poisson disk from CMYK channels of an image

Usage examples
--------------
* Use poisson-d module, from Grasshoper Python Script Component, to generate points of poisson disk 

.. code:: python

    import rhinoscriptsyntax as rs
    import imageio.v3 as iio
    from poisson_d import poisson_d as p

    # input variables: img_path, radius_min, radius_max, max_points, white_threshold
    # output variables: coordinates (list of Point3D), greys (list of floats)

    image = iio.imread(img_path)

    result = p.poisson_d_variant(
        img=image,
        radius_min_max=(radius_min, radius_max),
        max_points=max_points,
    )

    print(f"generated {len(result)} points")

    result = p.filter_out_white(image, result, white_threshold)

    coordinates = [rs.CreatePoint(pn.x, -pn.y, 0) for pn in result]
    greys = [x.grey for x in result]

* Use poisson-d module, from Grasshoper Python Script Component, to generate points of poisson disk on C, M, Y, K channels 

.. code:: python

    import rhinoscriptsyntax as rs
    import imageio.v3 as iio
    from poisson_d import poisson_d as p

    # input variables: img_path, radius_min, radius_max, max_points, white_threshold
    # output variables: c_points, m_points, y_points, k_points for coordinates; c, m, y, k for greyscales

    image = iio.imread(img_path)

    ((c_points, m_points, y_points, k_points), (c, m, y, k)) = poisson_d_cmyk(
        img=image,
        r=(radius_min, radius_max),
        cnt=max_points,
        th=white_threshold,
    )

Credits
-------

This package was initialized with Cookiecutter_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
