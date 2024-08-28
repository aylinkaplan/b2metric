from app.tasks import send_overdue_reminders, generate_weekly_reports


def test_send_overdue_reminders():
    try:
        result = send_overdue_reminders.apply_async()
        print("send_overdue_reminders task result:", result.get(timeout=10))
    except Exception as e:
        print(f"send_overdue_reminders task failed: {e}")


def test_generate_weekly_reports():
    try:
        result = generate_weekly_reports.apply_async()
        print("generate_weekly_reports task result:", result.get(timeout=10))
    except Exception as e:
        print(f"generate_weekly_reports task failed: {e}")


if __name__ == "__main__":
    print("Testing Celery tasks...")
    test_send_overdue_reminders()
    test_generate_weekly_reports()
