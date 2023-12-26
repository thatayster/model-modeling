from datetime import date

from retailer_store.model import Batch, OrderLine


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch(ref="batch-001", sku=sku, qty=batch_qty, eta=date.today()),
        OrderLine(order_id="order-001", sku=sku, qty=line_qty)
    )


def test_can_allocate_if_available_is_greater_than_required():
    large_batch, small_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=20, line_qty=2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_is_smaller_than_required():
    small_batch, large_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=2, line_qty=20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_batch_is_equal_to_required():
    large_batch, small_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=2, line_qty=2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_sku_do_not_match():
    batch = Batch(ref="batch-001", sku="SOME-TABLE", qty=10, eta=date.today())
    different_sku_orderline = OrderLine(order_id="order-001", sku="ANOTHER-TABLE", qty=1)
    assert batch.can_allocate(different_sku_orderline) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line(sku="NICE-SOFA", batch_qty=20, line_qty=2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

def test_allocation_is_idempotent():
    batch, line = make_batch_and_line(sku="NICE-SOFA", batch_qty=20, line_qty=2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18