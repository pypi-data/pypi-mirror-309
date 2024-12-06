from math import ceil, fabs, floor


def precise_rounding(value, uncertainty, uncertainty_digits=2):
    """
    Rounds a measurement value and its uncertainty to a specified number
    of significant digits.

    Args:
        value (float): The measurement value.
        uncertainty (float): The uncertainty of the measurement.
        uncertainty_digits (int, optional): The number of significant
            digits for the uncertainty. Defaults to 2.

    Returns:
        tuple: A tuple containing the rounded value and the rounded
            uncertainty as strings.

    Raises:
        ValueError: If uncertainty is negative.
        ValueError: If uncertainty_digits is less than 1.
        TypeError: If value or uncertainty cannot be converted to float.

    Examples:

        >>> precise_rounding(123.45678, 0.01234)
        ('123.457', '0.013')

        >>> precise_rounding(123.45678, 0.01009)
        ('123.457', '0.010')

        >>> precise_rounding(123.45678, 0.515, 1)
        ('123.5', '0.6')

        >>> precise_rounding(123.45678, 5.123)
        ('123.5', '5.2')

        >>> precise_rounding(123.456, 0)
        ('123.456', '0')
    """

    # Ensure the inputs can be converted to numbers
    #
    try:
        value = float(value)
    except ValueError:
        raise TypeError("value must be a number")
    try:
        value = float(value)
    except ValueError:
        raise TypeError("uncertainty must be a number")
    try:
        uncertainty_digits = int(uncertainty_digits)
    except ValueError:
        raise TypeError("uncertainty_digits must be a number")

    # Ensure the uncertainty and uncertainty_digits are valid
    #
    if uncertainty < 0:
        raise ValueError("uncertainty must be non-negative")
    if uncertainty_digits < 1:
        raise ValueError("uncertainty_digits must be at least 1")

    if uncertainty != 0:

        # Calculate the characteristic and mantissa of the uncertainty
        #
        mantissa = uncertainty
        characteristic = 0
        exponent = 1

        # Adjust characteristic and mantissa for values >= 1.0
        #
        while mantissa >= 1.0:
            characteristic += 1
            exponent = 10 ** characteristic
            mantissa = uncertainty / exponent

        # Adjust characteristic and mantissa for values < 0.1
        #
        while mantissa < 0.1:
            characteristic -= 1
            exponent = 10 ** characteristic
            mantissa = uncertainty / exponent

        factor = 10 ** uncertainty_digits
        threshold = 0.1 * exponent / factor

        # Round uncertainty up and down
        #
        uncertainty_rounded_up = exponent * ceil(mantissa * factor) / factor
        uncertainty_rounded_down = exponent * floor(mantissa * factor) / factor

        # Determine the rounded uncertainty
        #
        if fabs(uncertainty_rounded_down - uncertainty) <= threshold:
            uncertainty = uncertainty_rounded_down
        else:
            uncertainty = uncertainty_rounded_up

        # Normalize the mantissa to the range from 0.1 (inclusive)
        # to 1.0 (exclusive).
        #
        if mantissa == 1.0:
            characteristic += 1
            exponent = 10 ** characteristic
            mantissa = 0.1  # it would be necessary in future versions

        # Round value, notice that round() function "round half to even",
        # thus we use int() to proper "scientific" rounding.
        #
        # value_rounded = exponent * round(value / exponent * factor) / factor
        #
        ef = exponent / factor
        if value >= 0:
            value_rounded = ef * int(value / ef + 0.5)
        else:
            value_rounded = - ef * int(-value / ef + 0.5)

        # Format the rounded value and uncertainty as strings
        #
        if uncertainty != int(uncertainty):
            n_digits = uncertainty_digits - characteristic
            uncertainty_rounded_str = f"{uncertainty:.{n_digits}f}"
            value_rounded_str = f"{value_rounded:.{n_digits}f}"
        else:
            uncertainty_rounded_str = f"{uncertainty:.0f}"
            value_rounded_str = f"{value_rounded:.0f}"
            emitted_u_digits = len(uncertainty_rounded_str)
            if emitted_u_digits < uncertainty_digits:
                padding = "." + "0" * (uncertainty_digits - emitted_u_digits)
                uncertainty_rounded_str += padding
                value_rounded_str += padding

    else:
        # Handle the case where uncertainty is zero
        assert uncertainty == 0

        # uncertainty_rounded = uncertainty
        uncertainty_rounded_str = "0"
        value_rounded = value
        value_rounded_str = f"{value_rounded:f}"
        if "." in value_rounded_str:
            value_rounded_str = value_rounded_str.rstrip("0").rstrip(".")

    return value_rounded_str, uncertainty_rounded_str
