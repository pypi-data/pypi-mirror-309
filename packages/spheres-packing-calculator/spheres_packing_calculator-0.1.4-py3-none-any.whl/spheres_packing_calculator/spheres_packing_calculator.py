import numpy as np
from scipy.integrate import simpson
from pyvista import read
import os


def read_vtk_file(file):  # Returns data
    """
    Returns data object after reading a file with PyVista. Includes a check
    to ensure the file exists.

    Args:
        file (str): Path to the .vtk file.

    Returns:
        pyvista.DataSet: The data object from the .vtk file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file cannot be read as a PyVista dataset.
    """
    # Check if file exists
    if not os.path.isfile(file):
        raise FileNotFoundError(
            f"The file '{file}' does not exist. Please provide a valid path.")

    # Attempt to read the file
    try:
        data = read(file)
    except Exception as e:
        raise ValueError(f"Error reading the file '{file}': {e}")

    return data


def retrieve_coordinates(data):  # Returns x_data, y_data, z_data, radii
    """
    Extract x, y, z coordinates and radii from the dataset.

    Args:
        data: PyVista data object containing particle information.

    Returns:
        tuple: Arrays for x, y, z coordinates and radii.
    """
    x_data = data.points[:, 0]
    y_data = data.points[:, 1]
    z_data = data.points[:, 2]
    radii = data["radius"]
    return x_data, y_data, z_data, radii


def double_circle_intersection(r, a, b) -> float:
    """
    Function that calculates the cross sectional area of a circle intersected
    by two perpendicular lines. The cross section of a double and triple cap
    intersection forms this shape, which means its area can be used as an
    intermediary to find the volume of double and triple intersections of
    spherical caps.

    Circle has radius r, and the centre-chord distances are a and b

    :Example:
    >>> double_circle_intersection(2, 0, 0)
    3.141592653589793
    """
    # Evaluating cases
    if a**2 + b**2 < r**2:
        # a and b are contained within the circle, double intersection exists

        # Calculate the sector area (the area of the circle wedge)
        sector_area = 0.5 * r**2 * \
            (3*np.pi/2 + np.arcsin(a / r) + np.arcsin(b / r))

        # Calculate areas of the two remaining triangles
        triangle_area = 0.5 * a * \
            (np.sqrt(r**2 - a**2) - b) + 0.5 * b * (np.sqrt(r**2 - b**2) - a)

        # Circle area minus sector area and triangles
        intersection_area = np.pi*r**2 - sector_area - triangle_area

        return intersection_area
    else:
        # a and b outside or on circle
        # Special cases, a double intersection does not exist
        if (a >= 0 and b >= 0) or a >= r or b >= r:
            return 0  # No circle
        elif a <= -r and b <= -r:
            return np.pi*r**2  # Full circle
        # Segment with centre-chord distance = b
        elif (a < 0 and 0 < b < r) or (a <= -r and -r < b <= 0):
            return r**2 * (np.arccos(b/r) - (b/r) * np.sqrt(1 - (b/r)**2))
        # Segment with centre-chord distance = a
        elif (b < 0 and 0 < a < r) or (b <= -r and -r < a <= 0):
            return r**2 * (np.arccos(a/r) - (a/r) * np.sqrt(1 - (a/r)**2))
        elif -r < a < 0 and -r < b < 0:
            # Circle missing two minor segments, with centre-chord distances
            # -a and -b
            return np.pi*r**2 - (
                r**2 * (np.arccos(-b/r) + (b/r) * np.sqrt(1 - (b/r)**2))) - (
                r**2 * (np.arccos(-a/r) + (a/r) * np.sqrt(1 - (a/r)**2)))


def triple_cap_integrator(R, a, b,
                          c_lim_lower, c_lim_upper,
                          num_simpson_sample_points=6) -> float:
    """
    Function for integrating the differential volume of slices of a double
    spherical cap intersection. R is the radius of the sphere, a and b are the
    distances of two planes from the sphere's centre. c_lim_lower and
    c_lim_upper are the integration limits in the third dimension.
    """

    # 6 sample points, can be improved if you're being very precise
    c_values = np.linspace(c_lim_lower, c_lim_upper,
                           num=num_simpson_sample_points)
    radius_values = np.sqrt(R**2 - c_values**2)
    cross_sectional_area_values = np.array(
        [double_circle_intersection(r, a, b) for r in radius_values])

    # Integrate cross sectional slice throughout the volume
    volume = simpson(y=cross_sectional_area_values, x=c_values)
    return volume


def single_cap_intersection(R, a) -> float:
    """
    Function that evaluates the analytical volume of a spherical cap. The
    sphere has radius R, and the distance from the sphere's centre to the
    boundary is a.

    :Example:
    >>> single_cap_intersection(1, 0.2)
    1.47445415208481
    """
    return np.pi * (R - a)**2 * (2 * R + a) / 3


def double_cap_intersection(R, a, b) -> float:
    """
    Function that evaluates the volume of a double spherical cap intersection.
    The sphere has radius R, and the distances from the centre to the
    boundaries are a and b

    The cross sectional area function can safely just be integrated from -R
    to R. However, this may be wasteful as this can include regions where the
    cross sectional area is zero. The integration limits are set as small as
    possible, such that they just encapsulate the cap volume.

    :Example:
    >>> double_cap_intersection(1, 0.2, 0.3)
    0.3974826065772735
    """

    if a**2 + b**2 <= R**2:
        # a and b are contained within sphere, double cap intersection exists
        if a < 0 and b < 0:
            c_lim_upper = R
        elif a < 0:
            c_lim_upper = np.sqrt(R**2 - b**2)
        elif b < 0:
            c_lim_upper = np.sqrt(R**2 - a**2)
        else:
            c_lim_upper = np.sqrt(R**2 - a**2 - b**2)
    else:
        # Short-circuiting for cases which have analytical solutions
        # (perfect accuracy and reduces computational load)
        if a > 0 and b > 0:
            # No intersection
            return 0
        elif a < 0 and b > 0:
            # Single cap intersection, with centre-chord distance = b
            return np.pi * (R - b)**2 * (3 * R - (R - b)) / 3
        elif b < 0 and a > 0:
            # Single cap intersection, with centre-chord distance = a
            return np.pi * (R - a)**2 * (3 * R - (R - a)) / 3
        else:
            # Sphere missing two caps, with centre-chord distances -a and -b
            return 4/3 * np.pi * R**3 - (
                np.pi * (R + a)**2 * (3 * R - (R + a)) / 3) - (
                np.pi * (R + b)**2 * (3 * R - (R + b)) / 3)

    # The double cap intersection is symmetrical, so c_lim_lower is set to 0
    # and the volume doubled
    c_lim_lower = 0
    return 2*triple_cap_integrator(R, a, b, c_lim_lower, c_lim_upper,
                                   num_simpson_sample_points=3)


def triple_cap_intersection(R, a, b, c) -> float:
    """
    Function that evaluates the volume of a triple cap intersection. The sphere
    has radius R, and the distance from the sphere's centre to the boundaries
    are a, b and c.

    The cross sectional area function must now be carefully integrated to
    include the intersection with the boundary defined by c. The upper
    integration limit is set as low as possible, such that it still entirely
    encapsulates the cap volume. The lower integration limit is set as c,
    unless the cap is symmetrical (c <= -c_lim_upper) or there is no
    intersection (c >= c_lim_upper).

    :Example:
    >>> triple_cap_intersection(1, 0.3, 0.1, 0.2)
    0.16451538109365088
    """

    if a**2 + b**2 <= R**2:
        # a and b are contained within sphere
        # This means a triple cap intersection can exist (depending on c)
        if a < 0 and b < 0:
            c_lim_upper = R
        elif a < 0:
            c_lim_upper = np.sqrt(R**2 - b**2)
        elif b < 0:
            c_lim_upper = np.sqrt(R**2 - a**2)
        else:
            c_lim_upper = np.sqrt(R**2 - a**2 - b**2)
    else:
        # Short-circuiting for cases which have analytical solutions
        # (perfect accuracy and reduces computational load)
        if a > 0 and b > 0:
            # No intersection
            return 0
        elif a < 0 and b > 0:
            if c <= -np.sqrt(R**2 - b**2):
                # Single cap intersection, with centre-chord distance = b
                return np.pi * (R - b)**2 * (3 * R - (R - b)) / 3
            elif c >= np.sqrt(R**2 - b**2):
                # No intersection
                return 0
            else:
                c_lim_upper = np.sqrt(R**2 - b**2)
        elif b < 0 and a > 0:
            if c <= -np.sqrt(R**2 - a**2):
                # Single cap intersection, with centre-chord distance = a
                return np.pi * (R - a)**2 * (3 * R - (R - a)) / 3
            elif c >= np.sqrt(R**2 - a**2):
                # No intersection
                return 0
            else:
                c_lim_upper = np.sqrt(R**2 - a**2)
        elif c > 0 and a < -np.sqrt(R**2 - c**2) and b < -np.sqrt(R**2 - c**2):
            # Single cap intersection, with centre-chord distance = c
            return np.pi * (R - c)**2 * (3 * R - (R - c)) / 3
        elif b < 0 and a < 0:
            if c <= -max(np.sqrt(R**2 - a**2), np.sqrt(R**2 - b**2)):
                # Sphere missing three single caps, with centre-chord distances
                # -a, -b, and -c
                return 4/3 * np.pi * R**3 - (
                    np.pi * (R + a)**2 * (3 * R - (R + a)) / 3) - (
                    np.pi * (R + b)**2 * (3 * R - (R + b)) / 3) - (
                    np.pi * (R + c)**2 * (3 * R - (R + c)) / 3)
            else:
                c_lim_upper = R

    if c >= c_lim_upper:
        # No intersection
        return 0
    elif c <= -c_lim_upper:
        # Symmetrical -> double cap intersection
        c_lim_lower = -c_lim_upper
    else:
        # c intersects the double cap intersection
        # -> integrate between c and c_lim_upper
        c_lim_lower = c

    return triple_cap_integrator(R, a, b, c_lim_lower, c_lim_upper)


def compute_boundaries(x_data, y_data, z_data,
                       padding_factor=0.1):  # Returns boundaries
    """
    Compute the minimum and maximum boundaries for x, y, and z.
    """

    x_range, y_range, z_range = np.ptp(x_data), np.ptp(y_data), np.ptp(z_data)
    boundaries = {
        "x_min": min(x_data) + padding_factor * x_range,
        "x_max": max(x_data) - padding_factor * x_range,
        "y_min": min(y_data) + padding_factor * y_range,
        "y_max": max(y_data) - padding_factor * y_range,
        "z_min": min(z_data) + padding_factor * z_range,
        "z_max": max(z_data) - padding_factor * z_range,
    }
    return boundaries


def calculate_overlaps(x_data, y_data, z_data,
                       radii, boundaries):  # Returns overlaps
    """
    Calculate boolean masks for particles overlapping with each boundary.

    Args:
        x_data, y_data, z_data (np.ndarray): Arrays of particle x, y, z.
        radii (np.ndarray): Array of particle radii.
        boundaries (dict): Dictionary defining the boundary limits.

    Returns:
        dict: Boolean masks for overlaps with each boundary
        ('x_min', 'x_max', 'y_min', etc.).
    """
    overlaps = {
        "x_min": (x_data > boundaries["x_min"] - radii) &
                 (x_data < boundaries["x_min"] + radii),
        "x_max": (x_data > boundaries["x_max"] - radii) &
                 (x_data < boundaries["x_max"] + radii),
        "y_min": (y_data > boundaries["y_min"] - radii) &
                 (y_data < boundaries["y_min"] + radii),
        "y_max": (y_data > boundaries["y_max"] - radii) &
                 (y_data < boundaries["y_max"] + radii),
        "z_min": (z_data > boundaries["z_min"] - radii) &
                 (z_data < boundaries["z_min"] + radii),
        "z_max": (z_data > boundaries["z_max"] - radii) &
                 (z_data < boundaries["z_max"] + radii),
    }
    return overlaps


# Returns active_overlap_values
def calculate_active_overlap_values(total_particles, x_data, y_data, z_data,
                                    boundaries, overlaps):
    """
    Calculate the overlap distances for particles intersecting the boundaries.

    Args:
        total_particles (int): Total number of particles.
        x_data, y_data, z_data (np.ndarray): Arrays of particle coordinates.
        radii (np.ndarray): Array of particle radii.
        boundaries (dict): Dictionary defining the boundaries for x, y, and z.
        overlaps (dict): Dictionary of boolean masks indicating overlaps with
        boundaries.

    Returns:
        np.ndarray: Array of distances between particle centers and boundaries,
        or NaN for no overlap.
    """
    active_overlap_values = np.full((total_particles, 6), np.nan, dtype=float)

    active_overlap_values[:, 0] = np.where(
        overlaps["x_min"], boundaries["x_min"] - x_data, np.nan)
    active_overlap_values[:, 1] = np.where(
        overlaps["x_max"], x_data - boundaries["x_max"], np.nan)
    active_overlap_values[:, 2] = np.where(
        overlaps["y_min"], boundaries["y_min"] - y_data, np.nan)
    active_overlap_values[:, 3] = np.where(
        overlaps["y_max"], y_data - boundaries["y_max"], np.nan)
    active_overlap_values[:, 4] = np.where(
        overlaps["z_min"], boundaries["z_min"] - z_data, np.nan)
    active_overlap_values[:, 5] = np.where(
        overlaps["z_max"], z_data - boundaries["z_max"], np.nan)

    return active_overlap_values


def is_inside_boundaries(x_data, y_data, z_data,
                         boundaries, radii):  # Returns inside_mask
    """
    Determine which particles are completely inside the defined boundaries.

    Args:
        x_data, y_data, z_data (np.ndarray): Arrays containing the x, y, z
        coordinates of particles.
        boundaries (dict): Dictionary defining the boundaries for x, y, and z.
        radii (np.ndarray): Array of particle radii.

    Returns:
        np.ndarray: Boolean mask indicating whether each particle is inside
        the boundaries.
    """

    return (
        (x_data >= boundaries["x_min"] + radii) &
        (x_data <= boundaries["x_max"] - radii) &
        (y_data >= boundaries["y_min"] + radii) &
        (y_data <= boundaries["y_max"] - radii) &
        (z_data >= boundaries["z_min"] + radii) &
        (z_data <= boundaries["z_max"] - radii)
    )


# Returns outside_mask
def is_outside_boundaries(x_data, y_data, z_data, boundaries, radii):
    """
    Determine which particles are completely outside the defined boundaries.

    Args:
        x_data, y_data, z_data (np.ndarray): Arrays containing the x, y, z
        coordinates of particles.
        boundaries (dict): Dictionary defining the boundaries for x, y, and z.
        radii (np.ndarray): Array of particle radii.

    Returns:
        np.ndarray: Boolean mask indicating whether each particle is outside
        the boundaries.
    """

    return (
        (x_data <= boundaries["x_min"] - radii) |
        (x_data >= boundaries["x_max"] + radii) |
        (y_data <= boundaries["y_min"] - radii) |
        (y_data >= boundaries["y_max"] + radii) |
        (z_data <= boundaries["z_min"] - radii) |
        (z_data >= boundaries["z_max"] + radii)
    )


def calculate_particle_volume(i, total_particles, radii, inside_mask,
                              outside_mask, full_particle_volumes,
                              active_overlap_values, report_progress) -> float:
    """
    Calculate the volume contribution of a given particle.
    If the particle is fully within the boundaries, its entire volume is
    counted; likewise, if it is fully outside, no volume is counted.
    The main functionality lies between these two cases, where the volume of
    intersection between the particle and the boundary region is calculated.

    Args:
        i (int): Index of the particle being evaluated.
        total_particles (int): Total number of particles.
        radii (np.ndarray): Array of particle radii.
        inside_mask (np.ndarray): Boolean mask indicating particles completely
        inside the boundaries.
        outside_mask (np.ndarray): Boolean mask indicating particles completely
        outside the boundaries.
        full_particle_volumes (np.ndarray): Array of full particle volumes.
        active_overlap_values (np.ndarray): Array of overlap distances with
        boundaries.
        report_progress (bool): If True, prints progress during computation.

    Returns:
        float: The volume contribution of the particle.
    """
    if report_progress and i % (total_particles // 10) == 0:
        print(f'{i}/{total_particles}')

    # Check if particle is completely within boundaries
    if inside_mask[i]:
        return full_particle_volumes[i]  # Add full volume directly

    # Check if particle is completely outside boundaries
    # This check is necessary for particles which intersect the (infinite)
    # boundary planes but are outside the actual boundary region
    elif outside_mask[i]:
        return 0

    # Otherwise, calculate the partial volume that overlaps the boundary region
    else:
        # Initialise partial volume at zero
        partial_volume = 0

        # Create array of overlap distances, filtering NaN values for
        # non-overlapping boundaries
        overlap_values = active_overlap_values[i][~np.isnan(
            active_overlap_values[i])]

        # Calculate the number of overlaps per particle
        number_of_overlaps = len(overlap_values)

        # Determine partial volume depending on the number of boundaries
        if number_of_overlaps == 1:
            partial_volume = single_cap_intersection(
                radii[i], overlap_values[0])

        elif number_of_overlaps == 2:
            partial_volume = double_cap_intersection(
                radii[i], overlap_values[0], overlap_values[1])

        elif number_of_overlaps == 3:
            partial_volume = triple_cap_intersection(
                radii[i], overlap_values[0], overlap_values[1],
                overlap_values[2])

        # Return calculated particle volume
        return partial_volume


def compute_cell_volume(boundaries):
    """
    Calculate the volume of a cuboidal cell defined by its boundaries.

    Args:
        boundaries (dict): Dictionary containing the keys 'x_min', 'x_max',
        'y_min', 'y_max', 'z_min', and 'z_max', which define the cuboid's
        limits.

    Returns:
        float: The volume of the cuboid.
    """
    # Compute the lengths of the cuboid sides
    x_length = boundaries['x_max'] - boundaries['x_min']
    y_length = boundaries['y_max'] - boundaries['y_min']
    z_length = boundaries['z_max'] - boundaries['z_min']

    # Calculate the volume
    volume = x_length * y_length * z_length
    return volume


def compute_packing_density(file, boundaries=None, report_progress=False):
    """
    Compute the packing density of particles within a defined boundary region.

    Args:
        file (str): Path to the `.vtk` file containing particle data.
        boundaries (dict, optional): Dictionary defining the cuboidal region
        boundaries. If None, boundaries will be computed from the dataset.
        report_progress (bool, optional): If True, prints progress during
        computation.

    Returns:
        float: The packing density as the fraction of volume occupied by
        particles.
    """

    print(file)

    try:
        data = read_vtk_file(file)
        print('Successfully read file\n')
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as value_error:
        print(value_error)

    # Retrieve particle coordinates and radii
    x_data, y_data, z_data, radii = retrieve_coordinates(data)

    # Determine boundaries
    if boundaries is None:
        boundaries = compute_boundaries(x_data, y_data, z_data)
    # Calculate overlaps
    overlaps = calculate_overlaps(x_data, y_data, z_data, radii, boundaries)

    # Determine active overlap values
    total_particles = len(radii)
    active_overlap_values = calculate_active_overlap_values(
        total_particles, x_data, y_data, z_data, boundaries, overlaps
    )

    # Determine packing density
    total_particles = len(radii)

    # Pre-compute and store full particle volumes
    full_particle_volumes = (4/3) * np.pi * (radii)**3

    # Get masks for particles completely inside or outside boundaries
    inside_mask = is_inside_boundaries(
        x_data, y_data, z_data, boundaries, radii)
    outside_mask = is_outside_boundaries(
        x_data, y_data, z_data, boundaries, radii)

    total_particle_volume = sum(
        calculate_particle_volume(i, total_particles, radii, inside_mask,
                                  outside_mask, full_particle_volumes,
                                  active_overlap_values, report_progress)
        for i in range(total_particles)
    )

    cell_volume = compute_cell_volume(boundaries)

    packing_density = total_particle_volume/cell_volume

    return packing_density


if __name__ == "__main__":

    file = r"post\centered_fcc_packed_spheres_500000.vtk"

    boundaries = {
        "x_min": -0.2,
        "x_max": 0.2,
        "y_min": -0.2,
        "y_max": 0.2,
        "z_min": -0.2,
        "z_max": 0.2,
    }

    packing_density = compute_packing_density(file, boundaries)

    # Print outputs
    print(f'Packing density: {packing_density}')
    print(f'FCC packing max: {np.pi*np.sqrt(2)/6}')
    print(f'SC packing max:  {np.pi/6}')
