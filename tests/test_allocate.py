from datetime import date, timedelta

import pytest

from retailer_store.model import Batch, OrderLine, OutOfStock, allocate


def create_shifted_date(shift_in_days: int = 0) -> date:
    return date.today() + timedelta(days=shift_in_days)


def test_prefers_current_stock_batches_to_shipments():
    tomorrow = create_shifted_date(1)
    in_stock_batch = Batch(ref="in-stock-batch", sku="FANCY-CLOCK", qty=100, eta=None)
    shipment_batch = Batch(ref="shipment-batch", sku="FANCY-CLOCK", qty=100, eta=tomorrow)
    line = OrderLine(order_id="id", sku="FANCY-CLOCK", qty=10)

    selected_batch_ref = allocate(line, [in_stock_batch, shipment_batch])

    assert selected_batch_ref == in_stock_batch.reference
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    today = create_shifted_date()
    tomorrow = create_shifted_date(1)
    later = create_shifted_date(2) 
    earliest = Batch(ref="in-stock-batch", sku="FANCY-CLOCK", qty=100, eta=today)
    medium = Batch(ref="in-stock-batch", sku="FANCY-CLOCK", qty=100, eta=tomorrow)
    latest = Batch(ref="in-stock-batch", sku="FANCY-CLOCK", qty=100, eta=later)
    shipment_batch = Batch(ref="shipment-batch", sku="FANCY-CLOCK", qty=100, eta=tomorrow)
    line = OrderLine(order_id="id", sku="FANCY-CLOCK", qty=10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_raises_out_of_stock_exception_if_cannot_allocate():
    today = create_shifted_date()
    batch = Batch(ref="batch-ref", sku="FANCY-CLOCK", qty=10, eta=today)
    line1 = OrderLine(order_id="order-1", sku="FANCY-CLOCK", qty=10)
    line2 = OrderLine(order_id="order-2", sku="FANCY-CLOCK", qty=10)

    allocate(line1, [batch])

    with pytest.raises(OutOfStock):
        allocate(line2, [batch])