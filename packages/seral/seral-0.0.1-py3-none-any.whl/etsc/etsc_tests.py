import pytest
from unittest.mock import patch
import numpy as np
# from etsc import EvolvingTimeSeriesClustering
from seral import Cluster

def _generate_prototype(random: np.random.RandomState, alpha: float):
    crip_prototype_len: int = random.randint(10, 100)
    crisp_prototype = random.random(crip_prototype_len)
    start_idx: int = random.randint(0, 100)
    end_idx: int = start_idx + crip_prototype_len
    psv_len: int = random.randint(end_idx, end_idx + 100)
    psv = np.random.random(psv_len)
    psv[start_idx:end_idx] = crisp_prototype
    pcv = random.random(psv_len) * alpha
    pcv[start_idx] = alpha + 0.01
    pcv[end_idx - 1] = alpha + 0.01

    return psv, pcv, start_idx, end_idx, crisp_prototype


def test_new_cluster_defuzzification(random_seed: int = 42):
    """ Test whether the correct crisp prototype is returned."""
    # from etsc import new_cluster_get_crisp_prototype_boundaries
    import numpy as np

    # Arrange
    random = np.random.RandomState(random_seed)
    alpha: float = random.random()

    psv, pcv, start_idx, end_idx, crisp_prototype =_generate_prototype(random, alpha)

    cluster: Cluster = Cluster(psv, id=0, exclusion_zone=0.0)
    cluster.pcv = pcv
    cluster.alpha = alpha

    # Act
    result_start_idx, result_end_idx = cluster._get_crisp_prototype_boundaries()
    result_crisp_prototype = cluster._prototype_defuzzification()
    result_prototype_prop = cluster.prototype

    # Assert
    assert cluster.psv is psv, ("The PSV should be the same as the one passed to the constructor.")
    assert cluster.pcv is pcv, ("The PCV should be the same as the one passed to the constructor.")

    assert result_start_idx == start_idx, ("Returned start index is wrong.")
    assert result_end_idx == end_idx, ("Returned end index is wrong.")

    assert np.array_equal(result_crisp_prototype, crisp_prototype), (
        "The crisp prototype should be the same as the one "
        "passed to the constructor.")

    assert np.array_equal(result_prototype_prop, result_crisp_prototype), (
        "The prototype property should return the same as the "
        "get_crisp_prototype method.")


def test_new_cluster_defuzzification_repeated(random_seed: int = 42, runs: int = 100):
    """ Perform a number of runs of test_new_cluster_defuzzification() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_new_cluster_defuzzification(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_new_cluster_defuzzification failed at random seed {seed}", ae)


def test_get_alignment_for_psv(random_seed: int = 6265):
    """ Test whether the correct alignment is returned.
    
    The alignment returned should be such that the signal is optimally aligned to the PSV.
    """

    # Arrange
    random = np.random.RandomState(random_seed)
    alpha: float = random.random()

    psv, pcv, start_idx, end_idx, crisp_prototype =_generate_prototype(random, alpha)

    crisp_prototype_len = len(crisp_prototype)
    sample_start_idx = random.randint(0, crisp_prototype_len//4)
    sample_end_idx = random.randint(crisp_prototype_len//4, crisp_prototype_len)
    sample = crisp_prototype[sample_start_idx:sample_end_idx]

    cluster: Cluster = Cluster(psv, id=0, exclusion_zone=0.0)
    cluster.pcv = pcv
    cluster.alpha = alpha

    # Act
    result_alignment = cluster._get_alignment_of_sample_to_psv(sample)

    # Assert
    extracted_sample = psv[result_alignment:result_alignment + len(sample)]
    assert np.array_equal(extracted_sample, sample), ("The extracted sample should be the same as the one passed to the method.")


def test_get_alignment_for_psv_repeated(random_seed: int = 42, runs: int = 100):
    """ Perform a number of runs of test_get_alignment_for_psv() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_get_alignment_for_psv(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_get_alignment_for_psv failed at random seed {seed}. \nOriginal AssertionError: {ae}")


def test_add_sample_to_cluster(random_seed: int = 42):
    """ Test whether the sample is correctly added to the cluster. """
    pass


def test_generate_new_pcv(random_seed: int = 42):
    """ Test whether the new PCV is correctly generated. 
    
    The new PCV should reflect increased support for the region where the sample was added to the PSV.

    """
    # Arrange
    random = np.random.RandomState(random_seed)

    psv, pcv, start_idx, end_idx, crisp_prototype =_generate_prototype(random, alpha=0.5)

    cluster = Cluster(psv, id=0, exclusion_zone=0.0)
    cluster.pcv = pcv
    cluster.alpha = 0.5

    sample_start_idx = random.randint(0, len(crisp_prototype)//4)
    sample_end_idx = random.randint(len(crisp_prototype)//4, len(crisp_prototype))
    sample = crisp_prototype[sample_start_idx:sample_end_idx]

    # Act
    result_new_pcv = cluster._generate_new_pcv(start_idx=sample_start_idx, end_idx=sample_end_idx)
    # result_new_pcv_second = cluster._generate_new_pcv(start_idx=sample_start_idx, end_idx=sample_end_idx)

    # Assert
    assert np.all(result_new_pcv[:sample_start_idx]<pcv[:sample_start_idx]), ("The region outside the new sample should have decreased support.")
    assert np.all(result_new_pcv[sample_start_idx:sample_end_idx]>pcv[sample_start_idx:sample_end_idx]), ("The region where the new sample was added should have increased support.")
    assert np.all(result_new_pcv[sample_end_idx:]<pcv[sample_end_idx:]), ("The region outside the new sample should have decreased support.")


def test_generate_new_pcv_repeated(random_seed: int = 42, runs: int = 100):
    """ Perform a number of runs of test_generate_new_pcv() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_generate_new_pcv(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_generate_new_pcv failed at random seed {seed}. \nOriginal AssertionError: {ae}")


def test_generate_new_pcv_with_edge_alignment(random_seed:int = 42):
    """ Test whether the new PCV is correctly generated when the sample is aligned across the edge of the existing PSV.
    
    If the new alignment is such that the sample is aligned across the edge of the existing prototype, the new PCV should expand.
    
    """

    # Arrange
    random = np.random.RandomState(random_seed)

    previous_length = random.randint(10, 100)
    previous_pcv = random.random(previous_length)

    should_expand_left: bool = random.choice([True, False])
    should_expand_right: bool = random.choice([True, False])
    
    if should_expand_left and should_expand_right:
        sample_start_idx = random.randint(-100, -1)
        sample_end_idx = random.randint(previous_length+1, previous_length+100)
    elif not should_expand_left and not should_expand_right:
        sample_start_idx = random.randint(0, previous_length//3)
        sample_end_idx = random.randint(2*previous_length//3, previous_length)
    elif should_expand_left:
        sample_start_idx = random.randint(-100, -1)
        sample_end_idx = random.randint(0, previous_length//3)
    else:
        sample_start_idx = random.randint(2*previous_length//3, previous_length)
        sample_end_idx = random.randint(previous_length+1, previous_length+100)

    sample_length = sample_end_idx - sample_start_idx
    

    cluster = Cluster(np.random.random(previous_length), id=0, exclusion_zone=0.0)
    cluster.pcv = previous_pcv
    cluster.alpha = random.random()

    # Act
    result_new_pcv = cluster._generate_new_pcv(start_idx=sample_start_idx, end_idx=sample_end_idx)

    # Assert
    if should_expand_left or should_expand_right:
        assert len(result_new_pcv) > previous_length, ("The new PCV should be longer than the previous one.")

    if should_expand_left:
        assert np.all(result_new_pcv[:-sample_start_idx] == result_new_pcv[0]), "The left expansion should be uniform."

    if should_expand_right:
        assert np.all(result_new_pcv[-(sample_end_idx-previous_length):] == result_new_pcv[-1]), "The right expansion should be uniform."


def test_generate_new_pcv_with_edge_alignment_repeated(random_seed:int = 42, runs: int = 100):
    """ Perform a number of runs of test_generate_new_pcv_with_edge_alignment() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_generate_new_pcv_with_edge_alignment(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_generate_new_pcv_with_edge_alignment failed at random seed {seed}. \nOriginal AssertionError: {ae}")

""" Test whether the new PSV is correctly generated.
    
    Properties to test:
    - The new PSV should be of equal length to the input (synced) arrays
    - Wherever the input arrays had NaN values, the new prototype should have NaN values.
    - If the previous psv is all 0s, then the sign of the new prototype should be the same as sign of the input arrays.
    - If the number of points is set to 0, the new prototype should be the same as the input sample.
    - If the number of points is set to 1, the new prototype should be the mean of previous prototype and the input sample.
    - If the number of points is set to infinity, the new prototype should be the old prototype.
    """

def test_generate_new_psv_sum_without_nan(random_seed:int = 42):
    """ Test whether the sum calculation without NaN values is correct. 
    
    In this test, aligned sample and aligned PSV are generated such that there are no NaN values.
    The correctness of summation is tested under the following conditions:
    - Either one of the arrays is all zeros --> the result should be the other array divided by (number of points + 1)
    - One of the arrays is other one multiplied by -1, the number of points is set to 1 --> result should be all 0
    - The number of points is set to 1 --> result should be the mean of the two arrays
    - The number of points is set to 0 --> result should be the sample
    - The number of points is set to infinity --> result should be the prototype
    - Regardless of the number of points, if the two input arrays are equal, the result is equal
    """

    # Arrange
    random = np.random.RandomState(random_seed)
    aligned_length: int = random.randint(10, 100)
    signal_zeros = np.zeros(aligned_length)
    signal_random = random.random(aligned_length)
    signal_random_2 = random.random(aligned_length)
    signal_random_neg = -signal_random  

    # Act and Assert

    # Test 1:
    # - Prototype is set to all zeros
    # - Result should be the sample divided by (number of points + 1)
    cluster = Cluster(signal_zeros, id=0, exclusion_zone=0.0)
    number_of_points = random.randint(0, 100)
    cluster.number_of_points = number_of_points
    result = cluster._generate_new_psv(signal_random, signal_zeros)
    assert np.allclose(result, signal_random/(number_of_points+1)), ("The result should be similar to the sample.")

    # Test 2:
    # - Sample is set to all zeros
    # - Result should be the prototype multiplied by (number of points)/(number of points + 1)
    cluster = Cluster(signal_random, id=0, exclusion_zone=0.0)
    cluster.number_of_points = number_of_points
    result = cluster._generate_new_psv(signal_zeros, signal_random)
    assert np.allclose(result, signal_random*(number_of_points)/(number_of_points+1)), ("The result should be similar to the prototype.")

    # Test 3:
    # - Prototype is set to all zeros
    # - Sample is set to all zeros
    # - Result should be all zeros
    cluster = Cluster(signal_zeros, id=0, exclusion_zone=0.0)
    result = cluster._generate_new_psv(signal_zeros, signal_zeros)
    assert np.allclose(result, signal_zeros), ("The result should be all zeros.")

    # Test 4:
    # - The prototype is random
    # - The sample is the prototype multiplied by -1
    # - The number of points is set to 1
    # - The result should be all zeros
    cluster = Cluster(signal_random, id=0, exclusion_zone=0.0)
    cluster.number_of_points = 1
    result = cluster._generate_new_psv(signal_random_neg, signal_random)
    assert np.allclose(result, signal_zeros), ("The result should be all zeros.")

    # Test 5:
    # - The prototype is random
    # - The sample is random
    # - The number of points is set to 1
    # - The result should be the mean of the two arrays
    cluster = Cluster(signal_random, id=0, exclusion_zone=0.0)
    cluster.number_of_points = 1
    result = cluster._generate_new_psv(signal_random_2, signal_random)
    assert np.allclose(result, (signal_random + signal_random_2)/2), ("The result should be the mean of the two arrays.")

    # Test 6:
    # - The prototype is random
    # - The sample is random
    # - The number of points is set to 0
    # - The result should be the sample
    cluster = Cluster(signal_random_2, id=0, exclusion_zone=0.0)
    cluster.number_of_points = 0
    result = cluster._generate_new_psv(signal_random, signal_random_2)
    assert np.allclose(result, signal_random), ("The result should be the sample.")

    # Test 7:
    # - The prototype is random
    # - The sample is random
    # - The number of points is set to a huge number
    # - The result should be the prototype
    cluster = Cluster(signal_random_2, id=0, exclusion_zone=0.0)
    cluster.number_of_points = 1e10
    result = cluster._generate_new_psv(signal_random, signal_random_2)
    assert np.allclose(result, signal_random_2), ("The result should be the prototype.")

    # Test 8:
    # - The prototype is random
    # - The sample is equal to the prototype
    # - Regardless of the number of points, the result should be the prototype
    cluster = Cluster(signal_random, id=0, exclusion_zone=0.0)
    cluster.number_of_points = random.randint(0, 100)
    result = cluster._generate_new_psv(signal_random, signal_random)
    assert np.allclose(result, signal_random), ("The result should be the prototype.")




def _generate_aligned_sample_and_aligned_psv(random: np.random.RandomState, should_expand_left: bool, should_expand_right: bool) -> tuple[np.ndarray, np.ndarray]:
    """ Generate a sample and prototype that are aligned. 

    The sample and prototype are aligned such that the sample is a subsequence of the prototype.
    The alignment can be such that the sample is aligned across the edge of the prototype.

    :param random: RandomState object.
    :param should_expand_left: Whether the alignment should expand to the left.
    :param should_expand_right: Whether the alignment should expand to the right.
    :return: Tuple containing the aligned sample and aligned prototype
    
    """
    # Generate the prototype
    prototype_len = random.randint(10, 100)
    data = random.random(prototype_len)

    # Generate the "aligned" prootype
    # First generate a null prototype, then insert the prototype into it.
    aligned_prototype = np.full(prototype_len, np.nan)
    aligned_sample = np.full(prototype_len, np.nan)
    if should_expand_left and not should_expand_right:
        # prototype: --------xxxxxxxxxxxxxxxxxxxxxxxxx
        # sample:    xxxxxxxxxxxxxxxxxxxxxxxxx--------
        prototype_start_idx = random.randint(prototype_len//4, prototype_len//2)
        prototype_end_idx = prototype_len
        sample_start_idx = 0
        sample_end_idx = random.randint(prototype_start_idx, 3*prototype_len//4)
        assert sample_start_idx < prototype_start_idx < sample_end_idx < prototype_end_idx
    elif not should_expand_left and should_expand_right:
        # prototype: xxxxxxxxxxxxxxxxxxxxxxxxx--------
        # sample:    ------------xxxxxxxxxxxxxxxxxxxxx
        prototype_start_idx = 0
        prototype_end_idx = random.randint(prototype_len//2, 3*prototype_len//4)
        sample_start_idx = random.randint(prototype_len//4, prototype_end_idx)
        sample_end_idx = prototype_len
        assert prototype_start_idx < sample_start_idx < prototype_end_idx < sample_end_idx
    elif should_expand_left and should_expand_right:
        # prototype: ----xxxxxxxxxxxxxxxxxxxxx--------
        # sample:    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        prototype_start_idx = random.randint(prototype_len//4, prototype_len//3)
        prototype_end_idx = random.randint(prototype_start_idx+1, 2*prototype_len//3)
        sample_start_idx = 0
        sample_end_idx = prototype_len
        assert sample_start_idx < prototype_start_idx < prototype_end_idx < sample_end_idx
    else:
        # prototype: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # sample:    ----xxxxxxxxxxxxxxxxxxxxx--------
        prototype_start_idx = 0
        prototype_end_idx = prototype_len
        sample_start_idx = random.randint(1, prototype_len//4)
        sample_end_idx = random.randint(2*prototype_len//3, prototype_len)
        assert prototype_start_idx < sample_start_idx < sample_end_idx < prototype_end_idx
    
    aligned_prototype[prototype_start_idx:prototype_end_idx] = data[prototype_start_idx:prototype_end_idx]   
    aligned_sample[sample_start_idx:sample_end_idx] = data[sample_start_idx:sample_end_idx]

    assert len(aligned_prototype) == len(aligned_sample), ("The aligned prototype and aligned sample should have the same length.")

    return aligned_sample, aligned_prototype


def test_generate_new_psv_length(random_seed:int = 42):
    """ Test whether the new new PSV is of length equal to the input arrays. """
    
    # Arrange

    random = np.random.RandomState(random_seed)
    should_expand_left: bool = random.choice([True, False])
    should_expand_right: bool = random.choice([True, False])
    

    sample_aligned, previous_psv_aligned = _generate_aligned_sample_and_aligned_psv(random, should_expand_left, should_expand_right)

    
    cluster = Cluster(np.random.random(len(previous_psv_aligned)), id=0, exclusion_zone=0.0)

    # Act
    result_new_psv = cluster._generate_new_psv(sample_aligned, previous_psv_aligned)

    # Assert
    assert len(result_new_psv) == len(sample_aligned), ("The new prototype should have the same length as the input arrays.")
    

def test_generate_new_psv_length_repeated(random_seed:int = 42, runs: int = 100):
    """ Perform a number of runs of test_generate_new_psv_length() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_generate_new_psv_length(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_generate_new_psv_length failed at random seed {seed}. \nOriginal AssertionError: {ae}")
    

def test_generate_new_psv_nan_values(random_seed:int = 42):
    """ Test whether the new prototype has NaN values where the input arrays have NaN values. """

    # Arrange

    random = np.random.RandomState(random_seed)
    should_expand_left: bool = random.choice([True, False])
    should_expand_right: bool = random.choice([True, False])
    

    sample_aligned, previous_psv_aligned = _generate_aligned_sample_and_aligned_psv(random, should_expand_left, should_expand_right)

    
    cluster = Cluster(np.random.random(len(previous_psv_aligned)), id=0, exclusion_zone=0.0)

    # Act
    result_new_psv = cluster._generate_new_psv(sample_aligned, previous_psv_aligned)

    # Assert
    assert np.all(np.isnan(result_new_psv) == np.bitwise_and(np.isnan(sample_aligned), np.isnan(previous_psv_aligned))), ("The new prototype should have NaN values where the input arrays have NaN values.")


def test_generate_new_psv_nan_values_repeated(random_seed:int = 42, runs: int = 100):
    """ Perform a number of runs of test_generate_new_psv_nan_values() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_generate_new_psv_nan_values(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_generate_new_psv_nan_values failed at random seed {seed}. \nOriginal AssertionError: {ae}")
        
    
def test_generate_new_psv_sign(random_seed:int = 42):
    """ Test whether the new prototype has the same sign as the input arrays. """

    # Arrange

    random = np.random.RandomState(random_seed)
    should_expand_left: bool = random.choice([True, False])
    should_expand_right: bool = random.choice([True, False])
    

    sample_aligned, previous_psv_aligned = _generate_aligned_sample_and_aligned_psv(random, should_expand_left, should_expand_right)
    
    # set the previous prototype to all 0s where not nan
    previous_psv_aligned[np.logical_not(np.isnan(previous_psv_aligned))] = 0
    
    cluster = Cluster(np.random.random(len(previous_psv_aligned)), id=0, exclusion_zone=0.0)

    # Act
    result_new_psv = cluster._generate_new_psv(sample_aligned, previous_psv_aligned)

    # Assert
    mask = np.logical_and(np.logical_not(np.isnan(sample_aligned)), np.logical_not(np.isnan(previous_psv_aligned))) # Mask is required to ignore NaN values in inputs
    assert np.all(np.sign(result_new_psv[mask]) == np.sign(sample_aligned[mask])), ("The new prototype should have the same sign as the input arrays.")


def test_generate_new_psv_sign_repeated(random_seed:int = 42, runs: int = 100):
    """ Perform a number of runs of test_generate_new_psv_sign() """
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]
    for seed in random_seeds:
        try:
            test_generate_new_psv_sign(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_generate_new_psv_sign failed at random seed {seed}. \nOriginal AssertionError: {ae}")


def test_add_sample_increases_number_of_points(random_seed:int = 42):
    """ Test whether the number of points is correctly increased when a sample is added. """
    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(np.random.random(100), id=0, exclusion_zone=0.0)
    initial_number_of_points = random.randint(0, 100)
    cluster.number_of_points = initial_number_of_points
    cluster.add_sample(np.random.random(100))

    # Act
    result_number_of_points = cluster.number_of_points

    # Assert
    assert result_number_of_points == initial_number_of_points + 1, ("The number of points should be increased by 1.")


def test_add_sample_generates_valid_pcv_and_psv(random_seed:int = 42):
    """ Thest whether the new PCV and PSV are of the correct length """

    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(np.random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = np.random.random(100)
    cluster.alpha = random.random()
    cluster.number_of_points = random.randint(0, 100)

    sample = np.random.random(100)

    # Act
    cluster.add_sample(sample)

    # Assert
    assert len(cluster.pcv) == len(cluster.psv), ("The new PCV should have the same length as the new PSV.")


def test_add_multiple_samples_generates_valid_pcv_and_psv(random_seed:int = 42, n_samples: int = 100):
    """ Thest whether the new PCV and PSV are of the correct length """

    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(np.random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = np.random.random(100)
    cluster.alpha = random.random()
    cluster.number_of_points = random.randint(0, 100)

    for _ in range(n_samples):
        sample = np.random.random(100)

        # Act
        cluster.add_sample(sample)

        # Assert
        assert len(cluster.pcv) == len(cluster.psv), ("The new PCV should have the same length as the new PSV.")


def test_generate_psv_correctly_applies_weights(random_seed: int = 42):
    """ Test _generate_new_psv method for correctness of weighted summation. 
    
    The method applies a weight to the previous prototype and the new sample before summing them.
    However, the weight should not applied to all indices of the prototype and the sample.
    Since the prototype and the sample do not align perfectly, the weight shoud be applied only to the aligned indices. 
    At other indices, the weight should be 1.
    """

    # Arrange
    random = np.random.RandomState(random_seed)
    full_aligned_sample: np.ndarray = random.random(100)
    full_aligned_prototype: np.ndarray = random.random(100)
    
    aligned_sample: np.ndarray = full_aligned_sample.copy()
    aligned_prototype: np.ndarray = full_aligned_prototype.copy()

    sample_left_nans:int = random.randint(0, len(aligned_sample)//4)
    prototype_right_nans:int = random.randint(0, len(aligned_prototype)//4)

    aligned_sample[:sample_left_nans] = np.nan
    aligned_prototype[-prototype_right_nans:] = np.nan

    cluster = Cluster(np.random.random(100), id=0, exclusion_zone=0.0)
    cluster.number_of_points = 1 # The weights will be equal for the prototype and the sample

    # Act
    result_psv = cluster._generate_new_psv(aligned_sample, aligned_prototype)

    # Assert
    assert np.count_nonzero(np.isnan(result_psv)) == 0, ("The result should not have any NaN values.")

    # Check the left side of the result
    assert np.allclose(result_psv[:sample_left_nans], aligned_prototype[:sample_left_nans]), ("The left side of the result should be equal to the left side of the prototype.")

    # Check the right side of the result
    assert np.allclose(result_psv[-prototype_right_nans:], aligned_sample[-prototype_right_nans:]), ("The right side of the result should be equal to the right side of the sample.")

    # Check the middle of the result, it should be the average of the prototype and the sample
    assert np.allclose(result_psv[sample_left_nans:-prototype_right_nans], (aligned_prototype[sample_left_nans:-prototype_right_nans] + aligned_sample[sample_left_nans:-prototype_right_nans])/2), ("The middle of the result should be the average of the prototype and the sample.")

    pass

def test_copy():
    """ Test whether the copy method returns a deep copy of the cluster. """

    # Arrange
    cluster = Cluster(np.random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = np.random.random(100)
    cluster.alpha = np.random.random()
    cluster.number_of_points = np.random.randint(0, 100)

    # Act
    unaltered_copy = cluster.copy(deep=True)
    modified_copy = cluster.copy(deep=True)

    modified_copy.pcv = cluster.pcv + 1
    modified_copy.alpha = cluster.alpha / 2
    modified_copy.number_of_points = cluster.number_of_points + 1
    modified_copy.psv = cluster.psv + 1
    modified_copy.id = cluster.id + 1
    modified_copy.eral_exclusion_zone = (cluster.eral_exclusion_zone / 2) if cluster.eral_exclusion_zone!=0 else 1

    # Assert
    for key in cluster.__dict__:
        assert np.array_equal(cluster.__dict__[key], unaltered_copy.__dict__[key]), (f"The attribute {key} should not be mutated.")
        assert not np.array_equal(cluster.__dict__[key], modified_copy.__dict__[key]), (f"The attribute {key} should be mutated.")
    

def test_get_new_components_does_not_mutate_self(random_seed: int = 42):
    """ Check whether call to get_new_components does not mutate the cluster. """
    
    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = random.random(100)
    cluster.alpha = random.random()
    cluster.number_of_points = random.randint(0, 100)

    
    sample = random.random(100)

    cluster_copy = cluster.copy(deep=True)
    # Act
    cluster._get_new_components(sample)

    # Assert
    for key in cluster.__dict__:
        assert np.array_equal(cluster.__dict__[key], cluster_copy.__dict__[key]), (f"The attribute {key} should not be mutated.")


def test_merge_with_itself(random_seed: int = 42):
    """ If merging a cluster with itself, the result should be the same as the original cluster. """

    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = random.random(100)
    cluster.alpha = random.random()
    cluster.number_of_points = random.randint(1, 100)

    # Act
    original_cluster = cluster.copy(deep=True)
    other_cluster = cluster.copy(deep=True)

    cluster.try_merge(other_cluster)

    # Assert
    for key in cluster.__dict__:
        if key == "number_of_points":
            continue
        assert np.allclose(cluster.__dict__[key], original_cluster.__dict__[key]), (f"The attribute {key} should not be mutated.")
    
    assert cluster.number_of_points == 2*original_cluster.number_of_points, ("The number of points should be doubled.")

def test_merge_with_empty(random_seed: int = 42):
    """ If merging with an empty cluster, the result should be the same as the original cluster. """

    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = random.random(100)
    cluster.alpha = random.random()
    cluster.number_of_points = random.randint(1, 100)

    other_cluster = Cluster(random.random(100), id=1, exclusion_zone=0.0)
    other_cluster.pcv = random.random(100)
    other_cluster.alpha = random.random()
    other_cluster.number_of_points = 0

    # Act
    original_cluster = cluster.copy(deep=True)
    cluster.try_merge(other_cluster)

    # Assert
    for key in cluster.__dict__:
        assert np.allclose(cluster.__dict__[key], original_cluster.__dict__[key]), (f"The attribute {key} should not be mutated.")


def test_merge_when_empty(random_seed: int = 42):
    """ When merging an empty cluster with another cluster, the result should be the same as the other cluster. """
    # Arrange
    random = np.random.RandomState(random_seed)
    cluster = Cluster(random.random(100), id=0, exclusion_zone=0.0)
    cluster.pcv = random.random(100)
    cluster.alpha = random.random()
    cluster.number_of_points = 0

    other_cluster = Cluster(random.random(100), id=1, exclusion_zone=0.0)
    other_cluster.pcv = random.random(100)
    other_cluster.alpha = random.random()
    other_cluster.number_of_points = random.randint(1, 100)

    # Act
    original_cluster = cluster.copy(deep=True)
    merge_result = cluster.try_merge(other_cluster, min_new_length=0.0)
    assert merge_result, ("The merge should be successful.")

    # Assert
    for key in cluster.__dict__:
        if key in ["id", "alpha"]:
            continue
        assert np.allclose(cluster.__dict__[key], other_cluster.__dict__[key]), (f"The attribute {key} should be the same as the other cluster.")
    
    assert cluster.id == original_cluster.id, ("The ID should be the same as the original cluster.")
    assert cluster.alpha == original_cluster.alpha, ("The alpha should be the same as the other cluster.")


def test_merge_two_equal_crisp_prototypes(random_seed: int = 42):
    """ Merge two clusters with equal crisp prototypes. """

    # Arrange
    random = np.random.RandomState(random_seed)
    alpha = random.random()
    psv, pcv, start_idx, end_idx, crisp_prototype = _generate_prototype(random, alpha=alpha)
    cluster = Cluster(psv, id=0, alpha=alpha, exclusion_zone=0.0)
    cluster.pcv = pcv
    cluster.number_of_points = 1
    
    other_psv = psv.copy()
    other_pcv = pcv.copy()
    other_psv[0:start_idx] = random.random(start_idx)
    other_psv[end_idx:] = random.random(len(other_psv) - end_idx)
    other_pcv[0:start_idx] = random.random(start_idx)*alpha
    other_pcv[end_idx:] = random.random(len(other_pcv) - end_idx)*alpha
    other_cluster = Cluster(other_psv, id=1, alpha=alpha, exclusion_zone=0.0)
    other_cluster.pcv = other_pcv
    other_cluster.number_of_points = 1

    # Act
    original_cluster = cluster.copy(deep=True)

    cluster.try_merge(other_cluster)

    # Assert
    assert cluster.number_of_points == 2, ("The number of points should be doubled.")
    assert np.allclose(cluster.prototype, original_cluster.prototype), ("The prototype should not be changed.")	   
    assert np.allclose(cluster.psv[:start_idx], (original_cluster.psv[:start_idx]+other_psv[0:start_idx])/2), ("The left side of the PSV should be the average of the two clusters.")
    assert np.allclose(cluster.psv[end_idx:], (original_cluster.psv[end_idx:]+other_psv[end_idx:])/2), ("The right side of the PSV should be the average of the two clusters.")
    assert np.allclose(cluster.pcv[:start_idx], (original_cluster.pcv[:start_idx]+other_pcv[0:start_idx])/2), ("The left side of the PCV should be the average of the two clusters.")
    assert np.allclose(cluster.pcv[end_idx:], (original_cluster.pcv[end_idx:]+other_pcv[end_idx:])/2), ("The right side of the PCV should be the average of the two clusters.")
    assert np.allclose(cluster.pcv[start_idx:end_idx], original_cluster.pcv[start_idx:end_idx]), ("The support in the middle should stay the same.")


def test_merge_with_crisp_only(random_seed: int = 42):
    """ Merge cluster with another cluster which has the same prototype, but it's PSV is equal to the crisp prototype prototype. """

    # Arrange
    random = np.random.RandomState(random_seed)
    alpha = random.random()
    psv, pcv, start_idx, end_idx, crisp_prototype = _generate_prototype(random, alpha=alpha)
    cluster = Cluster(psv, id=0, alpha=alpha, exclusion_zone=0.0)
    cluster.pcv = pcv
    cluster.number_of_points = 1

    other_psv = crisp_prototype.copy()
    other_pcv = pcv.copy()
    other_pcv = other_pcv[start_idx:end_idx]
    other_cluster = Cluster(other_psv, id=1, alpha=alpha, exclusion_zone=0.0)
    other_cluster.pcv = other_pcv
    other_cluster.number_of_points = 1

    assert np.allclose(other_cluster.prototype, cluster.prototype), ("The prototypes should be the same.")

    # Act
    original_cluster = cluster.copy(deep=True)

    cluster.try_merge(other_cluster)

    # Assert
    assert cluster.number_of_points == 2, ("The number of points should be doubled.")
    assert np.allclose(cluster.prototype, original_cluster.prototype), ("The prototype should not be changed.")
    assert np.allclose(cluster.psv, original_cluster.psv), ("The PSV should not be changed.")
    assert np.allclose(cluster.pcv[start_idx:end_idx], original_cluster.pcv[start_idx:end_idx]), ("The central part of PCV should not be changed.")
    assert np.allclose(cluster.pcv[:start_idx], original_cluster.pcv[:start_idx]/2), ("The left side of the PCV should be halved.")
    assert np.allclose(cluster.pcv[end_idx:], original_cluster.pcv[end_idx:]/2), ("The right side of the PCV should be halved.")


def test_merge_with_inverse_psv(random_seed: int = 42):
    """ Merge two clusters with inverse PSVs. """
    """ When merging two clusters with inverse PSVs, the result should have a psv of all zeros. """
    # Arrange
    random = np.random.RandomState(random_seed)
    
    """ We mock the alignment function to force it to return 0 shift. """
    with patch("seral.get_score_and_shift") as mock_get_score_and_shift:
        alpha = random.random()
        psv, pcv, start_idx, end_idx, crisp_prototype = _generate_prototype(random, alpha=alpha)
        cluster = Cluster(psv, id=0, alpha=alpha, exclusion_zone=0.0)
        cluster.pcv = pcv
        cluster.number_of_points = 1

        other_psv = -psv
        other_pcv = pcv.copy()
        other_cluster = Cluster(other_psv, id=1, alpha=alpha, exclusion_zone=0.0)
        other_cluster.pcv = other_pcv
        other_cluster.number_of_points = 1

        assert np.allclose(other_cluster.prototype, -cluster.prototype), ("The prototypes should negatives of each other same.")

        # Act
        original_cluster = cluster.copy(deep=True)

    
        mock_get_score_and_shift.return_value = (0, 0)
        cluster.try_merge(other_cluster)

    # Assert
    assert cluster.number_of_points == original_cluster.number_of_points + other_cluster.number_of_points, ("The number of points should be doubled.")
    assert np.allclose(cluster.prototype, np.zeros_like(cluster.prototype)), ("The prototype should be all zeros.")


def test_merge_with_single_sample(random_seed: int = 42):
    """ If merging a cluster with another cluster which has a single sample, the result should be the same if adding the sample to the cluster. """
    # Arrange
    random = np.random.RandomState(random_seed)
    alpha = random.random()
    psv, pcv, start_idx, end_idx, crisp_prototype = _generate_prototype(random, alpha=alpha)
    cluster = Cluster(psv, id=0, alpha=alpha, exclusion_zone=0.0)
    cluster.pcv = pcv
    cluster.number_of_points = random.randint(1, 100)

    sample = random.random(random.randint(10, 100))
    other_cluster = Cluster(sample, id=1, alpha=alpha, exclusion_zone=0.0)
    other_cluster.pcv = np.ones_like(sample)
    other_cluster.number_of_points = 1

    # Act
    original_cluster = cluster.copy(deep=True)

    merge_result = cluster.try_merge(other_cluster, min_new_length=0.0)
    assert merge_result, ("The merge should be successful.")        

    original_cluster.add_sample(sample)

    # Assert
    assert cluster.number_of_points == original_cluster.number_of_points, ("The number of points should be the same.")
    assert np.allclose(cluster.prototype, original_cluster.prototype), ("The prototype should be the same.")
    assert np.allclose(cluster.psv, original_cluster.psv), ("The PSV should be the same.")
    assert np.allclose(cluster.pcv, original_cluster.pcv), ("The PCV should be the same.")


def test_merge_repeat(random_seed: int = 42, runs: int = 100):
    rng = np.random.RandomState(random_seed)
    random_seeds: list[int] = [rng.randint(0, 10000) for _ in range(runs)]

    for seed in random_seeds:
        try:
            test_merge_with_itself(seed)
            test_merge_with_empty(seed)
            test_merge_when_empty(seed)
            test_merge_with_crisp_only(seed)
            test_merge_with_inverse_psv(seed)
            test_merge_with_single_sample(seed)
        except AssertionError as ae:
            raise AssertionError(f"test_merge failed at random seed {seed}. \nOriginal AssertionError: {ae}")

if __name__ == "__main__":
    pytest.main(["-v", __file__])