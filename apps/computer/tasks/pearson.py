from celery import shared_task
from scipy.stats import stats

from apps.computer.models.pearson import DataModel, PCorrelationModel


def get_mean(vectors):
    temp_arr = []
    for x in [v.get('value') for v in vectors]:
        if isinstance(x, (int, float)):
            temp_arr.append(x)
    return sum(temp_arr) / len(temp_arr)


@shared_task
def compute_pcorrelation(data, intersection_only=True) -> None:
    """
    Computes Pearson correlation.

    Parameters
    ----------
    intersection_only: bool
        Use only intersected area (not to use any `inputer`)
    data: dict
        Values to compose the vectors and pass to correlation computer.
    """

    # Get vectors
    x_vector = data.get('x', [])
    y_vector = data.get('y', [])

    # If no data was provided for both vectors
    if not x_vector and y_vector:
        return

    # Handle missing values (!!! can be threaded later !!!)
    x_mean = get_mean(x_vector)
    y_mean = get_mean(y_vector)

    # If only intersection is asked
    if intersection_only:
        vec1, vec2 = [], []

        # Get intersection by dates
        [(vec1.append(x.get('value') if isinstance(x.get('value'), (float, int)) else x_mean),
          vec2.append(y.get('value') if isinstance(y.get('value'), (float, int)) else y_mean))
         for x in x_vector for y in y_vector if x.get('date') == y.get('date')]

        # Pearson’s correlation coefficient and probability value.
        value, p_value = stats.pearsonr(vec1, vec2)

    # Non-intersection mode will be implemented in the future
    else:
        raise NotImplementedError('[x] This functionality is to be implemented in the future')

    # Create data point.
    data_instance = DataModel.objects.create(user_id=data.get('user_id'),
                                             x_data_type=data.get('x_data_type'),
                                             y_data_type=data.get('y_data_type'))
    # Create correlation.
    PCorrelationModel.objects.create(data=data_instance, value=value, p_value=p_value)
