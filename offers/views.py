from django.shortcuts import render, get_object_or_404
from .models import Offer
from collections import Counter
from django.utils.translation import get_language


def estimate_rating_distribution(avg_rating, total_votes):
    """
    Генерирует приближённое распределение оценок по среднему и кол-ву голосов.
    """

    # Исходные веса (можно подправить)
    base = {
        5: 0.78,
        4: 0.17,
        3: 0.03,
        2: 0.01,
        1: 0.01
    }

    # Скорректируем пятёрки, чтобы средняя сошлась
    def adjust_to_average(base, target_avg):
        max_iters = 1000
        for _ in range(max_iters):
            avg = sum(star * weight for star, weight in base.items())
            diff = target_avg - avg

            if abs(diff) < 0.001:
                break

            # Поправка только если безопасно
            if diff > 0:
                if base[4] >= 0.01:
                    base[5] += 0.01
                    base[4] -= 0.01
            else:
                if base[5] >= 0.01:
                    base[5] -= 0.01
                    base[4] += 0.01

        # Обрезаем отрицательные значения (на всякий случай)
        for k in base:
            if base[k] < 0:
                base[k] = 0

        total = sum(base.values())
        return {k: v / total for k, v in base.items()}

    weights = adjust_to_average(base, avg_rating)

    # Преобразуем в целые числа
    raw_counts = {k: int(v * total_votes) for k, v in weights.items()}
    # Корректируем погрешность (чтобы сумма ровно совпала)
    current_total = sum(raw_counts.values())
    raw_counts[5] += total_votes - current_total

    # Переведём в проценты
    percentages = {str(k): round(v / total_votes * 100, 1) for k, v in raw_counts.items()}
    print(percentages)
    return percentages


def offer_detail(request, slug):
    offer = get_object_or_404(Offer, slug=slug)
    reviews = offer.reviews.order_by('-date')

    translated_reviews = []
    lang = get_language()

    for r in reviews:
        translated_reviews.append({
            "name": r.name,
            "avatar": r.avatar,
            "rating": r.rating,
            "date": r.date,
            "text": r.get_translated_text(lang)
        })

    rating_percentages = estimate_rating_distribution(offer.rating, offer.votes_count)
    distribution_rows = [
        {"stars": str(i), "percent": rating_percentages[str(i)]}
        for i in range(5, 0, -1)
    ]
    print(distribution_rows)

    return render(request, 'offers/html/offer_detail.html', {
        'offer': offer,
        'reviews': translated_reviews,
        'distribution_rows': distribution_rows,
    })
