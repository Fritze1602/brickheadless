from content.schema import Collection
import cms


def inject_multi_collections(request):
    """
    Macht multi_collections global in allen Templates verfügbar (für Sidebar etc.).
    """
    collections = [
        obj
        for obj in cms.__dict__.values()
        if isinstance(obj, Collection) and not getattr(obj, "unique", False)
    ]

    return {"multi_collections": collections}
