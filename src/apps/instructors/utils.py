from .models import Instructor


def get_master_instructor_social_media():
    """
    Retrieves the social media IDs of the master instructor.

    :return: A dictionary containing the Instagram, YouTube, and Telegram IDs of the master instructor,
             or None if no master instructor is found.
    """
    master_instructor = Instructor.objects.filter(is_master=True).first()

    if master_instructor:
        instagram_social_media = master_instructor.instagram_id
        youtube_social_media = master_instructor.youtube_id
        telegram_social_media = master_instructor.telegram_id

        return {
            'instagram_id': instagram_social_media,
            'youtube_id': youtube_social_media,
            'telegram_id': telegram_social_media,
        }
    return None
